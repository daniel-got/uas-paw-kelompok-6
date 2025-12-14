"""Get all reviews by tourist"""
from pyramid.view import view_config
from sqlalchemy import select

from models.review_model import Review
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="review_by_tourist", request_method="GET", renderer="json")
@jwt_validate
def review_by_tourist(request):
    """
    GET /api/reviews/tourist/{touristId}
    Get all reviews by tourist
    
    Response (200 OK):
    [
        {
            "id": "uuid",
            "packageId": "uuid",
            "touristId": "uuid",
            "bookingId": "uuid",
            "rating": 5,
            "comment": "Amazing experience!",
            "createdAt": "2024-11-20T10:00:00Z",
            "package": {
                "id": "uuid",
                "name": "Maldives Paradise Retreat"
            }
        }
    ]
    """
    try:
        tourist_id = request.matchdict.get("touristId")
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        if not tourist_id:
            request.response.status = 400
            return {"error": "Tourist ID is required"}
        
        # Authorization check - tourist can only access own reviews
        if user_role == "tourist" and tourist_id != user_id:
            request.response.status = 403
            return {"error": "Forbidden"}
        
        db_session = request.dbsession
        query = select(Review).where(Review.tourist_id == tourist_id).order_by(Review.created_at.desc())
        result = db_session.execute(query)
        reviews = result.scalars().all()
        
        return [
            {
                "id": str(r.id),
                "packageId": str(r.package_id),
                "touristId": str(r.tourist_id),
                "bookingId": str(r.booking_id) if r.booking_id else None,
                "rating": r.rating,
                "comment": r.comment,
                "createdAt": r.created_at.isoformat() if r.created_at else None,
                "package": {
                    "id": str(r.package.id),
                    "name": r.package.name
                } if r.package else None
            }
            for r in reviews
        ]
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
