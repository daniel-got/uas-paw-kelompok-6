"""Upload payment proof"""
import os
import uuid as uuid_lib
from datetime import datetime
from pyramid.view import view_config
from sqlalchemy import select
from PIL import Image
from io import BytesIO

from models.booking_model import Booking
from helpers.jwt_validate_helper import jwt_validate

# Storage configuration
STORAGE_DIR = "storage/payment_proofs"
ALLOWED_EXTENSIONS = {"jpeg", "png", "jpg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@view_config(route_name="booking_payment_upload", request_method="POST", renderer="json")
@jwt_validate
def booking_payment_upload(request):
    """
    POST /api/bookings/{id}/payment-proof
    Upload payment proof (Tourist only)
    
    Request (multipart/form-data):
    - file: <image file> (JPG, PNG, max 5MB)
    
    Response (200 OK):
    {
        "id": "uuid",
        "packageId": "uuid",
        "touristId": "uuid",
        "travelDate": "2025-02-15",
        "travelersCount": 2,
        "totalPrice": 7000.0,
        "status": "pending",
        "createdAt": "2024-12-01T10:00:00Z",
        "completedAt": null,
        "hasReviewed": false,
        "paymentStatus": "pending_verification",
        "paymentProofUrl": "https://storage.com/proofs/uuid-here.jpg",
        "paymentProofUploadedAt": "2024-12-06T10:00:00Z",
        "paymentVerifiedAt": null,
        "paymentRejectionReason": null
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only tourists can upload payment proofs
        if user_role != "tourist":
            request.response.status = 403
            return {"error": "Only tourists can upload payment proof"}
        
        booking_id = request.matchdict.get("id")
        db_session = request.dbsession
        
        if not booking_id:
            request.response.status = 400
            return {"error": "ID is required"}
        
        # Validate file upload - accept both "proof" and "file" field names
        payment_file = None
        if "proof" in request.POST:
            payment_file = request.POST["proof"]
        elif "file" in request.POST:
            payment_file = request.POST["file"]
        else:
            request.response.status = 400
            return {"error": "Payment proof file is required"}
        
        if not hasattr(payment_file, 'file'):
            request.response.status = 400
            return {"error": "Invalid file upload"}
        
        # Validate file type
        allowed_types = ("image/jpeg", "image/png", "image/gif")
        content_type = getattr(payment_file, 'content_type', '') or getattr(payment_file, 'type', '')
        
        if content_type not in allowed_types:
            request.response.status = 400
            return {"error": f"Payment proof must be image file (jpeg, png, or gif). Got: {content_type}"}
        
        # Read file data
        image_data = payment_file.file.read()
        file_size = len(image_data)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            request.response.status = 400
            return {"error": "Payment proof file size must be <= 5MB"}
        
        # Validate it's a valid image
        try:
            image = Image.open(BytesIO(image_data))
            image.verify()
        except Exception:
            request.response.status = 400
            return {"error": "Invalid image file"}
        
        # Get booking
        query = select(Booking).where(Booking.id == booking_id)
        result = db_session.execute(query)
        booking = result.scalar_one_or_none()
        
        if not booking:
            request.response.status = 404
            return {"error": "Booking not found"}
        
        # Authorization check - tourist can only upload for own bookings
        if str(booking.tourist_id) != user_id:
            request.response.status = 403
            return {"error": "Forbidden"}
        
        # Check booking payment status
        if booking.payment_status not in ["unpaid", "rejected"]:
            request.response.status = 400
            return {"error": "Cannot upload payment proof for this booking"}
        
        # Create storage directory if it doesn't exist
        os.makedirs(STORAGE_DIR, exist_ok=True)
        
        # Generate unique filename
        file_ext = payment_file.filename.split('.')[-1]
        unique_filename = f"{booking_id}_{uuid_lib.uuid4()}.{file_ext}"
        filepath = os.path.join(STORAGE_DIR, unique_filename)
        
        # Save file
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Update booking
        booking.payment_proof_url = f"/payment_proofs/{unique_filename}"
        booking.payment_proof_uploaded_at = datetime.now()
        booking.payment_status = "pending_verification"
        
        db_session.flush()
        db_session.commit()
        
        return {
            "id": str(booking.id),
            "packageId": str(booking.package_id),
            "touristId": str(booking.tourist_id),
            "travelDate": booking.travel_date.isoformat(),
            "travelersCount": booking.travelers_count,
            "totalPrice": float(booking.total_price),
            "status": booking.status,
            "createdAt": booking.created_at.isoformat() if booking.created_at else None,
            "completedAt": booking.completed_at.isoformat() if booking.completed_at else None,
            "hasReviewed": booking.has_reviewed,
            "paymentStatus": booking.payment_status,
            "paymentProofUrl": booking.payment_proof_url,
            "paymentProofUploadedAt": booking.payment_proof_uploaded_at.isoformat() if booking.payment_proof_uploaded_at else None,
            "paymentVerifiedAt": booking.payment_verified_at.isoformat() if booking.payment_verified_at else None,
            "paymentRejectionReason": booking.payment_rejection_reason
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
