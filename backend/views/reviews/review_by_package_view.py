"""Get all reviews for a package"""
from pyramid.view import view_config
from sqlalchemy import select

from models.review_model import Review


@view_config(route_name="review_by_package", request_method="GET", renderer="json")
def review_by_package(request):
    """
    GET /api/reviews/package/{packageId}
    Get all reviews for a package
    
    Response (200 OK):
    [
        {
            "id": "uuid",
            "packageId": "uuid",
            "touristId": "uuid",
            "bookingId": "uuid",
            "rating": 5,
            "comment": "Amazing experience! Highly recommended.",
            "createdAt": "2024-11-20T10:00:00Z",
            "tourist": {
                "id": "uuid",
                "name": "John Doe"
            }
        }
    ]
    """
    try:
        package_id = request.matchdict.get("packageId")
        
        if not package_id:
            request.response.status = 400
            return {"error": "Package ID is required"}
        
        db_session = request.dbsession
        query = select(Review).where(Review.package_id == package_id).order_by(Review.created_at.desc())
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
                "tourist": {
                    "id": str(r.tourist.id),
                    "name": r.tourist.name
                } if r.tourist else None
            }
            for r in reviews
        ]
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
