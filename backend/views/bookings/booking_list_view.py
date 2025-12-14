"""Get all bookings with filters"""
import json
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import select, and_
from datetime import datetime

from models.booking_model import Booking
from models.package_model import Package
from models.user_model import User
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="bookings", request_method="GET", renderer="json")
@jwt_validate
def bookings_list(request):
    """
    GET /api/bookings
    Get all bookings with optional filters
    
    Query Parameters:
    - tourist_id (optional): Filter by tourist
    - package_id (optional): Filter by package
    - status (optional): Filter by status (pending, confirmed, cancelled, completed)
    - payment_status (optional): Filter by payment status (unpaid, pending_verification, verified, rejected)
    
    Response:
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
            "paymentProofUrl": "https://...",
            "paymentProofUploadedAt": "2024-12-01T12:00:00Z",
            "paymentVerifiedAt": "2024-12-01T14:00:00Z",
            "paymentRejectionReason": null,
            "package": {"id": "uuid", "name": "..."},
            "tourist": {"id": "uuid", "name": "...", "email": "..."}
        }
    ]
    """
    try:
        db_session = request.dbsession
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Base query
        query = select(Booking)
        
        # Apply filters
        filters = []
        
        # Role-based access
        if user_role == "tourist":
            filters.append(Booking.tourist_id == user_id)
        
        # Optional filters
        tourist_id = request.params.get("tourist_id")
        if tourist_id:
            filters.append(Booking.tourist_id == tourist_id)
        
        package_id = request.params.get("package_id")
        if package_id:
            filters.append(Booking.package_id == package_id)
        
        status = request.params.get("status")
        if status:
            filters.append(Booking.status == status)
        
        payment_status = request.params.get("payment_status")
        if payment_status:
            filters.append(Booking.payment_status == payment_status)
        
        if filters:
            query = query.where(and_(*filters))
        
        result = db_session.execute(query)
        bookings = result.scalars().all()
        
        return {
            "data": [
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
                    "paymentRejectionReason": b.payment_rejection_reason,
                    "package": {
                        "id": str(b.package.id),
                        "name": b.package.name,
                        "images": b.package.images[:1] if b.package.images else []
                    } if b.package else None,
                    "tourist": {
                        "id": str(b.tourist.id),
                        "name": b.tourist.name,
                        "email": b.tourist.email
                    } if b.tourist else None
                }
                for b in bookings
            ]
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
