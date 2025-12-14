"""Get pending payment verifications"""
from pyramid.view import view_config
from sqlalchemy import select

from models.booking_model import Booking
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="booking_payment_pending", request_method="GET", renderer="json")
@jwt_validate
def booking_payment_pending(request):
    """
    GET /api/bookings/payment/pending
    Get all bookings with pending payment verification (Agent only)
    
    Response (200 OK):
    [
        {
            "id": "uuid",
            "packageId": "uuid",
            "touristId": "uuid",
            "travelDate": "2025-02-15",
            "travelersCount": 2,
            "totalPrice": 7000.0,
            "status": "pending",
            "createdAt": "2024-12-01T10:00:00Z",
            "paymentStatus": "pending_verification",
            "paymentProofUrl": "https://storage.com/proofs/uuid-here.jpg",
            "paymentProofUploadedAt": "2024-12-06T10:00:00Z",
            "package": {
                "id": "uuid",
                "name": "Maldives Paradise Retreat"
            },
            "tourist": {
                "id": "uuid",
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
    ]
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only agents can see pending payments
        if user_role != "agent":
            request.response.status = 403
            return {"error": "Only agents can view pending payments"}
        
        db_session = request.dbsession
        
        # Get all pending payment bookings for agent's packages
        from sqlalchemy import and_
        from models.package_model import Package
        
        query = select(Booking).join(Package).where(
            and_(
                Booking.payment_status == "pending_verification",
                Package.agent_id == user_id
            )
        )
        
        result = db_session.execute(query)
        bookings = result.scalars().all()
        
        return [
            {
                "id": str(b.id),
                "packageId": str(b.package_id),
                "touristId": str(b.tourist_id),
                "travelDate": b.travel_date.isoformat(),
                "travelersCount": b.travelers_count,
                "totalPrice": float(b.total_price),
                "status": b.status,
                "createdAt": b.created_at.isoformat() if b.created_at else None,
                "paymentStatus": b.payment_status,
                "paymentProofUrl": b.payment_proof_url,
                "paymentProofUploadedAt": b.payment_proof_uploaded_at.isoformat() if b.payment_proof_uploaded_at else None,
                "package": {
                    "id": str(b.package.id),
                    "name": b.package.name
                },
                "tourist": {
                    "id": str(b.tourist.id),
                    "name": b.tourist.name,
                    "email": b.tourist.email
                }
            }
            for b in bookings
        ]
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
