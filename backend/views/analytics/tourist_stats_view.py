"""Get tourist dashboard statistics"""
from pyramid.view import view_config
from sqlalchemy import select, and_

from models.booking_model import Booking
from models.review_model import Review
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="analytics_tourist_stats", request_method="GET", renderer="json")
@jwt_validate
def analytics_tourist_stats(request):
    """
    GET /api/analytics/tourist/stats
    Get tourist dashboard statistics
    
    Response (200 OK):
    {
        "totalBookings": 8,
        "confirmedBookings": 5,
        "pendingBookings": 2,
        "completedBookings": 1,
        "cancelledBookings": 0,
        "totalSpent": 25600.0,
        "reviewsGiven": 1,
        "wishlistCount": 3
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only tourists can access tourist analytics
        if user_role != "tourist":
            request.response.status = 403
            return {"error": "Only tourists can access tourist analytics"}
        
        db_session = request.dbsession
        
        # Get all bookings for tourist
        query_bookings = select(Booking).where(Booking.tourist_id == user_id)
        result_bookings = db_session.execute(query_bookings)
        bookings = result_bookings.scalars().all()
        
        total_bookings = len(bookings)
        confirmed_bookings = len([b for b in bookings if b.status == "confirmed"])
        pending_bookings = len([b for b in bookings if b.status == "pending"])
        completed_bookings = len([b for b in bookings if b.status == "completed"])
        cancelled_bookings = len([b for b in bookings if b.status == "cancelled"])
        
        # Total spent
        total_spent = sum(float(b.total_price) for b in bookings if b.status in ["confirmed", "completed"])
        
        # Reviews given
        query_reviews = select(Review).where(Review.tourist_id == user_id)
        result_reviews = db_session.execute(query_reviews)
        reviews = result_reviews.scalars().all()
        reviews_given = len(reviews)
        
        # TODO: Implement wishlist if needed
        # For now, returning 0 as wishlist is not in the database model
        wishlist_count = 0
        
        return {
            "totalBookings": total_bookings,
            "confirmedBookings": confirmed_bookings,
            "pendingBookings": pending_bookings,
            "completedBookings": completed_bookings,
            "cancelledBookings": cancelled_bookings,
            "totalSpent": round(total_spent, 2),
            "reviewsGiven": reviews_given,
            "wishlistCount": wishlist_count
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
