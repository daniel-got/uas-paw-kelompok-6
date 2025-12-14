"""Get agent dashboard statistics"""
from pyramid.view import view_config
from sqlalchemy import select, func, and_

from models.booking_model import Booking
from models.package_model import Package
from models.review_model import Review
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="analytics_agent_stats", request_method="GET", renderer="json")
@jwt_validate
def analytics_agent_stats(request):
    """
    GET /api/analytics/agent/stats
    Get agent dashboard statistics
    
    Response (200 OK):
    {
        "totalPackages": 15,
        "totalBookings": 234,
        "pendingBookings": 12,
        "confirmedBookings": 198,
        "completedBookings": 20,
        "cancelledBookings": 4,
        "totalRevenue": 456789.5,
        "averageRating": 4.7,
        "pendingPaymentVerifications": 5
    }
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only agents can access agent analytics
        if user_role != "agent":
            request.response.status = 403
            return {"error": "Only agents can access agent analytics"}
        
        db_session = request.dbsession
        
        # Total packages
        query_total_packages = select(func.count(Package.id)).where(Package.agent_id == user_id)
        total_packages = db_session.execute(query_total_packages).scalar() or 0
        
        # Get all bookings for agent's packages
        query_bookings = select(Booking).join(Package).where(Package.agent_id == user_id)
        result_bookings = db_session.execute(query_bookings)
        bookings = result_bookings.scalars().all()
        
        total_bookings = len(bookings)
        pending_bookings = len([b for b in bookings if b.status == "pending"])
        confirmed_bookings = len([b for b in bookings if b.status == "confirmed"])
        completed_bookings = len([b for b in bookings if b.status == "completed"])
        cancelled_bookings = len([b for b in bookings if b.status == "cancelled"])
        
        # Total revenue (confirmed + completed)
        total_revenue = sum(
            float(b.total_price) for b in bookings 
            if b.status in ["confirmed", "completed"]
        )
        
        # Average rating
        query_avg_rating = select(func.avg(Review.rating)).select_from(Review).join(
            Package
        ).where(Package.agent_id == user_id)
        avg_rating = db_session.execute(query_avg_rating).scalar()
        avg_rating = float(avg_rating) if avg_rating else 0
        
        # Pending payment verifications
        pending_payments = len([b for b in bookings if b.payment_status == "pending_verification"])
        
        return {
            "totalPackages": total_packages,
            "totalBookings": total_bookings,
            "pendingBookings": pending_bookings,
            "confirmedBookings": confirmed_bookings,
            "completedBookings": completed_bookings,
            "cancelledBookings": cancelled_bookings,
            "totalRevenue": round(total_revenue, 2),
            "averageRating": round(avg_rating, 2),
            "pendingPaymentVerifications": pending_payments
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
