"""Get booking by ID"""
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select

from models.booking_model import Booking
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="booking_detail", request_method="GET", renderer="json")
@jwt_validate
def booking_detail(request):
    """
    GET /api/bookings/{id}
    Get booking by ID
    
    Response (200 OK):
    {
        "id": "uuid",
        "packageId": "uuid",
        "touristId": "uuid",
        "travelDate": "2025-02-15",
        "travelersCount": 2,
        "totalPrice": 7000.0,
        "status": "confirmed",
        "createdAt": "2024-12-01T10:00:00Z",
        "completedAt": null,
        "hasReviewed": false,
        "paymentStatus": "verified",
        "paymentProofUrl": "https://...",
        "paymentProofUploadedAt": "2024-12-01T12:00:00Z",
        "paymentVerifiedAt": "2024-12-01T14:00:00Z",
        "paymentRejectionReason": null
    }
    """
    try:
        booking_id = request.matchdict.get("id")
        db_session = request.dbsession
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        if not booking_id:
            request.response.status = 400
            return {"error": "ID is required"}
        
        query = select(Booking).where(Booking.id == booking_id)
        result = db_session.execute(query)
        booking = result.scalar_one_or_none()
        
        if not booking:
            request.response.status = 404
            return {"error": "Booking not found"}
        
        # Authorization check
        if user_role == "tourist" and str(booking.tourist_id) != user_id:
            request.response.status = 403
            return {"error": "Forbidden"}
        
        # If agent, check if they own the package
        if user_role == "agent":
            if str(booking.package.agent_id) != user_id:
                request.response.status = 403
                return {"error": "Forbidden"}
        
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
