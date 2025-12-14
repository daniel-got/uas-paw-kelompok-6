"""Create new booking"""
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select
from datetime import datetime, timedelta, date
import json

from models.booking_model import Booking
from models.package_model import Package
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="bookings", request_method="POST", renderer="json")
@jwt_validate
def booking_create(request):
    """
    POST /api/bookings
    Create new booking (Tourist only)
    
    Request Body:
    {
        "packageId": "uuid",
        "travelDate": "2025-02-15",
        "travelersCount": 2,
        "totalPrice": 7000.0
    }
    
    Response (201 Created):
    {
        "id": "uuid",
        "packageId": "uuid",
        "touristId": "uuid-from-token",
        "travelDate": "2025-02-15",
        "travelersCount": 2,
        "totalPrice": 7000.0,
        "status": "pending",
        "createdAt": "2024-12-06T10:00:00Z",
        "completedAt": null,
        "hasReviewed": false,
        "paymentStatus": "unpaid",
        "paymentProofUrl": null,
        "paymentProofUploadedAt": null,
        "paymentVerifiedAt": null,
        "paymentRejectionReason": null
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only tourists can create bookings
        if user_role != "tourist":
            request.response.status = 403
            return {"error": "Only tourists can create bookings"}
        
        # Parse request body
        try:
            body = request.json_body
        except (ValueError, json.JSONDecodeError):
            request.response.status = 400
            return {"error": "Invalid JSON body"}
        
        db_session = request.dbsession
        
        # Validate required fields
        package_id = body.get("packageId")
        travel_date_str = body.get("travelDate")
        travelers_count = body.get("travelersCount")
        total_price = body.get("totalPrice")
        
        if not all([package_id, travel_date_str, travelers_count, total_price]):
            request.response.status = 400
            return {"error": "Missing required fields"}
        
        # Validate travel date is at least 3 days in future
        try:
            travel_date = datetime.fromisoformat(travel_date_str).date()
            min_date = date.today() + timedelta(days=3)
            if travel_date < min_date:
                request.response.status = 400
                return {"error": "Travel date must be at least 3 days in the future"}
        except (ValueError, AttributeError):
            request.response.status = 400
            return {"error": "Invalid travel date format. Use YYYY-MM-DD"}
        
        # Validate travelers count
        try:
            travelers_count = int(travelers_count)
            if travelers_count < 1:
                request.response.status = 400
                return {"error": "Travelers count must be at least 1"}
        except (ValueError, TypeError):
            request.response.status = 400
            return {"error": "Travelers count must be a valid number"}
        
        # Validate total price
        try:
            total_price = float(total_price)
            if total_price <= 0:
                request.response.status = 400
                return {"error": "Total price must be greater than 0"}
        except (ValueError, TypeError):
            request.response.status = 400
            return {"error": "Total price must be a valid number"}
        
        # Check if package exists
        query = select(Package).where(Package.id == package_id)
        result = db_session.execute(query)
        package = result.scalar_one_or_none()
        
        if not package:
            request.response.status = 404
            return {"error": "Package not found"}
        
        # Validate travelers count doesn't exceed package max
        if travelers_count > package.max_travelers:
            request.response.status = 400
            return {"error": f"Travelers count cannot exceed {package.max_travelers}"}
        
        # Create booking
        booking = Booking(
            package_id=package_id,
            tourist_id=user_id,
            travel_date=travel_date,
            travelers_count=travelers_count,
            total_price=total_price,
            status="pending",
            payment_status="unpaid"
        )
        
        db_session.add(booking)
        db_session.flush()
        db_session.commit()
        
        request.response.status = 201
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
