"""Verify payment proof"""
from pyramid.view import view_config
from sqlalchemy import select
from datetime import datetime

from models.booking_model import Booking
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="booking_payment_verify", request_method="PUT", renderer="json")
@jwt_validate
def booking_payment_verify(request):
    """
    PUT /api/bookings/{id}/payment-verify
    Verify payment (Agent only)
    
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
        "paymentProofUrl": "https://storage.com/proofs/uuid-here.jpg",
        "paymentProofUploadedAt": "2024-12-06T10:00:00Z",
        "paymentVerifiedAt": "2024-12-06T11:00:00Z",
        "paymentRejectionReason": null
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only agents can verify payments
        if user_role != "agent":
            request.response.status = 403
            return {"error": "Only agents can verify payments"}
        
        booking_id = request.matchdict.get("id")
        db_session = request.dbsession
        
        if not booking_id:
            request.response.status = 400
            return {"error": "ID is required"}
        
        # Get booking
        query = select(Booking).where(Booking.id == booking_id)
        result = db_session.execute(query)
        booking = result.scalar_one_or_none()
        
        if not booking:
            request.response.status = 404
            return {"error": "Booking not found"}
        
        # Authorization check - agent can only verify own package bookings
        if str(booking.package.agent_id) != user_id:
            request.response.status = 403
            return {"error": "Forbidden"}
        
        # Check booking payment status
        if booking.payment_status != "pending_verification":
            request.response.status = 400
            return {"error": "Booking payment status is not pending verification"}
        
        # Update payment
        booking.payment_status = "verified"
        booking.payment_verified_at = datetime.now()
        booking.status = "confirmed"
        booking.payment_rejection_reason = None
        
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
