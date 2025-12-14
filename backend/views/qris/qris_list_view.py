"""Get all QRIS entries"""
import json
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.qris_model import Qris


@view_config(route_name="qris", request_method="GET", renderer="json")
def qris_list(request):
    """
    GET /api/qris
    Get all QRIS entries yang sudah diupload dengan pagination
    
    Query Parameters:
    - page (optional, default: 1): Page number
    - limit (optional, default: 10): Items per page
    
    Response:
    {
        "data": [
            {
                "id": "uuid",
                "static_qris_string": "00020126...",
                "dynamic_qris_string": "00020126...",
                "foto_qr_path": "storage/qris/filename.png",
                "fee_type": "rupiah",
                "fee_value": 10000,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 10,
            "total": 50
        }
    }
    """
    try:
        # Get pagination params
        page = int(request.params.get("page", 1))
        limit = int(request.params.get("limit", 10))
        
        # Validate pagination
        page = max(1, page)
        limit = max(1, min(limit, 100))  # Max 100 items per page
        
        offset = (page - 1) * limit
        
        # Build query
        query = select(Qris).offset(offset).limit(limit)
        
        # Get database session
        db_session = request.dbsession
        
        # Execute query
        result = db_session.execute(query)
        qris_list = result.scalars().all()
        
        # Get total count
        count_query = select(Qris)
        count_result = db_session.execute(count_query)
        total = len(count_result.scalars().all())
        
        # Format response
        data = []
        for qris in qris_list:
            data.append({
                "id": str(qris.id),
                "static_qris_string": qris.static_qris_string,
                "dynamic_qris_string": qris.dynamic_qris_string,
                "foto_qr_path": qris.foto_qr_path,
                "fee_type": qris.fee_type,
                "fee_value": float(qris.fee_value) if qris.fee_value else None,
                "created_at": qris.created_at.isoformat() if qris.created_at else None,
            })
        
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
            }
        }
    
    except Exception as e:
        request.response.status = 400
        return {"error": str(e)}
