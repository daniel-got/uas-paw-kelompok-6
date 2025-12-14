"""Create review"""
from pyramid.view import view_config
from sqlalchemy import select
import json

from models.review_model import Review
from models.booking_model import Booking
from models.package_model import Package
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="reviews", request_method="POST", renderer="json")
@jwt_validate
def review_create(request):
    """
    POST /api/reviews
    Create review (Tourist only, after completed trip)
    
    Request Body:
    {
        "packageId": "uuid",
        "bookingId": "uuid",
        "rating": 5,
        "comment": "Amazing experience! The package was well organized and the destination was breathtaking."
    }
    
    Response (201 Created):
    {
        "id": "uuid",
        "packageId": "uuid",
        "touristId": "uuid-from-token",
        "bookingId": "uuid",
        "rating": 5,
        "comment": "Amazing experience! The package was well organized...",
        "createdAt": "2024-12-06T10:00:00Z"
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only tourists can create reviews
        if user_role != "tourist":
            request.response.status = 403
            return {"error": "Only tourists can create reviews"}
        
        # Parse request body
        try:
            body = request.json_body
        except (ValueError, json.JSONDecodeError):
            request.response.status = 400
            return {"error": "Invalid JSON body"}
        
        db_session = request.dbsession
        
        # Validate required fields
        package_id = body.get("packageId")
        booking_id = body.get("bookingId")
        rating = body.get("rating")
        comment = body.get("comment")
        
        if not all([package_id, booking_id, rating, comment]):
            request.response.status = 400
            return {"error": "Missing required fields"}
        
        # Validate rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                request.response.status = 400
                return {"error": "Rating must be between 1 and 5"}
        except (ValueError, TypeError):
            request.response.status = 400
            return {"error": "Rating must be a number"}
        
        # Validate comment
        if len(str(comment).strip()) < 10:
            request.response.status = 400
            return {"error": "Comment must be at least 10 characters"}
        
        # Verify package exists
        query_pkg = select(Package).where(Package.id == package_id)
        result_pkg = db_session.execute(query_pkg)
        package = result_pkg.scalar_one_or_none()
        
        if not package:
            request.response.status = 404
            return {"error": "Package not found"}
        
        # Verify booking exists and belongs to tourist
        query_booking = select(Booking).where(Booking.id == booking_id)
        result_booking = db_session.execute(query_booking)
        booking = result_booking.scalar_one_or_none()
        
        if not booking:
            request.response.status = 404
            return {"error": "Booking not found"}
        
        # Verify booking belongs to tourist
        if str(booking.tourist_id) != user_id:
            request.response.status = 403
            return {"error": "Forbidden"}
        
        # Verify booking is for this package
        if str(booking.package_id) != str(package_id):
            request.response.status = 400
            return {"error": "Booking does not match package"}
        
        # Verify booking is completed
        if booking.status != "completed":
            request.response.status = 400
            return {"error": "Booking must be completed to leave a review"}
        
        # Verify booking hasn't been reviewed
        if booking.has_reviewed:
            request.response.status = 400
            return {"error": "This booking has already been reviewed"}
        
        # Create review
        review = Review(
            package_id=package_id,
            tourist_id=user_id,
            booking_id=booking_id,
            rating=rating,
            comment=comment
        )
        
        # Update booking
        booking.has_reviewed = True
        
        db_session.add(review)
        db_session.flush()
        db_session.commit()
        
        request.response.status = 201
        return {
            "id": str(review.id),
            "packageId": str(review.package_id),
            "touristId": str(review.tourist_id),
            "bookingId": str(review.booking_id),
            "rating": review.rating,
            "comment": review.comment,
            "createdAt": review.created_at.isoformat() if review.created_at else None
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
