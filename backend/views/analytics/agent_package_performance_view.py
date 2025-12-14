"""Get top performing packages"""
from pyramid.view import view_config
from sqlalchemy import select, func, and_

from models.package_model import Package
from models.booking_model import Booking
from models.review_model import Review
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="analytics_agent_package_performance", request_method="GET", renderer="json")
@jwt_validate
def analytics_agent_package_performance(request):
    """
    GET /api/analytics/agent/package-performance
    Get top performing packages
    
    Query Parameters:
    - limit (optional, default: 5): Top N packages
    
    Response (200 OK):
    [
        {
            "packageId": "uuid",
            "packageName": "Maldives Paradise Retreat",
            "bookingsCount": 45,
            "revenue": 157500.0,
            "averageRating": 4.8
        }
    ]
    """
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        # Only agents can access agent analytics
        if user_role != "agent":
            request.response.status = 403
            return {"error": "Only agents can access agent analytics"}
        
        # Get limit parameter
        limit = int(request.params.get("limit", 5))
        if limit < 1 or limit > 100:
            limit = 5
        
        db_session = request.dbsession
        
        # Get all packages for agent
        query_packages = select(Package).where(Package.agent_id == user_id)
        result_packages = db_session.execute(query_packages)
        packages = result_packages.scalars().all()
        
        package_stats = []
        
        for package in packages:
            # Get bookings for package (confirmed + completed only)
            query_bookings = select(Booking).where(
                and_(
                    Booking.package_id == package.id,
                    Booking.status.in_(["confirmed", "completed"])
                )
            )
            result_bookings = db_session.execute(query_bookings)
            bookings = result_bookings.scalars().all()
            
            bookings_count = len(bookings)
            revenue = sum(float(b.total_price) for b in bookings)
            
            # Get average rating for package
            query_avg_rating = select(func.avg(Review.rating)).where(
                Review.package_id == package.id
            )
            avg_rating = db_session.execute(query_avg_rating).scalar()
            avg_rating = float(avg_rating) if avg_rating else 0
            
            package_stats.append({
                "packageId": str(package.id),
                "packageName": package.name,
                "bookingsCount": bookings_count,
                "revenue": round(revenue, 2),
                "averageRating": round(avg_rating, 2)
            })
        
        # Sort by revenue descending
        package_stats.sort(key=lambda x: x["revenue"], reverse=True)
        
        return package_stats[:limit]
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
