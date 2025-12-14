"""Get bookings by package"""
from pyramid.view import view_config
from sqlalchemy import select

from models.booking_model import Booking
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="booking_by_package", request_method="GET", renderer="json")
@jwt_validate
def booking_by_package(request):
    """
    GET /api/bookings/package/{packageId}
    Get bookings by package
    
    Response (200 OK):
    [
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
            "paymentProofUrl": "url",
            "paymentProofUploadedAt": "2024-12-01T12:00:00Z",
            "paymentVerifiedAt": "2024-12-01T14:00:00Z",
            "paymentRejectionReason": null
        }
    ]
    """
    try:
        package_id = request.matchdict.get("packageId")
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        if not package_id:
            request.response.status = 400
            return {"error": "Package ID is required"}
        
        # Authorization check - agent can only access own package bookings
        if user_role == "agent":
            from models.package_model import Package
            
            query_pkg = select(Package).where(Package.id == package_id)
            result_pkg = request.dbsession.execute(query_pkg)
            package = result_pkg.scalar_one_or_none()
            
            if not package or str(package.agent_id) != user_id:
                request.response.status = 403
                return {"error": "Forbidden"}
        
        db_session = request.dbsession
        query = select(Booking).where(Booking.package_id == package_id)
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
                "completedAt": b.completed_at.isoformat() if b.completed_at else None,
                "hasReviewed": b.has_reviewed,
                "paymentStatus": b.payment_status,
                "paymentProofUrl": b.payment_proof_url,
                "paymentProofUploadedAt": b.payment_proof_uploaded_at.isoformat() if b.payment_proof_uploaded_at else None,
                "paymentVerifiedAt": b.payment_verified_at.isoformat() if b.payment_verified_at else None,
                "paymentRejectionReason": b.payment_rejection_reason
            }
            for b in bookings
        ]
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
