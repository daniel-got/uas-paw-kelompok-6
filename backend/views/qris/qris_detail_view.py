"""Get and delete QRIS by ID (no update allowed - QRIS is read-only after creation)"""
import base64
import io
import json
from pyramid.view import view_config
from sqlalchemy import select
import qrcode

from models.qris_model import Qris
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="qris_detail", request_method="GET", renderer="json")
def qris_detail(request):
    """
    GET /api/qris/{id}
    Get QRIS detail by ID
    
    Response (200 OK):
    {
        "id": "uuid",
        "nama": "Pembayaran Paket A",
        "jumlah_bayar": 1000000,
        "status": "aktif",
        "fee_type": "rupiah",
        "fee_value": 10000,
        "static_qris_string": "00020126...",
        "dynamic_qris_string": "00020126...",
        "foto_qr": "base64string",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    """
    try:
        qris_id = request.matchdict.get("id")
        
        if not qris_id:
            request.response.status = 400
            return {"error": "ID is required"}
        
        db_session = request.dbsession
        query = select(Qris).where(Qris.id == qris_id)
        result = db_session.execute(query)
        qris = result.scalar_one_or_none()
        
        if not qris:
            request.response.status = 404
            return {"error": "QRIS not found"}
        
        return {
            "id": str(qris.id),
            "static_qris_string": qris.static_qris_string,
            "dynamic_qris_string": qris.dynamic_qris_string,
            "foto_qr_path": qris.foto_qr_path,
            "fee_type": qris.fee_type,
            "fee_value": float(qris.fee_value) if qris.fee_value else None,
            "created_at": qris.created_at.isoformat() if qris.created_at else None,
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}


@view_config(route_name="qris_detail", request_method="DELETE", renderer="json")
@jwt_validate
def qris_delete(request):
    """
    DELETE /api/qris/{id}
    Delete QRIS by ID
    
    Response (200 OK):
    {
        "message": "QRIS berhasil dihapus"
    }
    """
    try:
        qris_id = request.matchdict.get("id")
        
        if not qris_id:
            request.response.status = 400
            return {"error": "ID is required"}
        
        db_session = request.dbsession
        query = select(Qris).where(Qris.id == qris_id)
        result = db_session.execute(query)
        qris = result.scalar_one_or_none()
        
        if not qris:
            request.response.status = 404
            return {"error": "QRIS not found"}
        
        db_session.delete(qris)
        db_session.flush()
        db_session.commit()
        
        return {"message": "QRIS berhasil dihapus"}
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
