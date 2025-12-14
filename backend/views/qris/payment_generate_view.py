"""Generate payment with amount from QRIS"""
import json
import os
import uuid
from io import BytesIO
from pyramid.view import view_config
from sqlalchemy import select, desc
import qrcode

from helpers.qris_helper import generate_dynamic_qris_string
from helpers.jwt_validate_helper import jwt_validate
from models.qris_model import Qris

# Storage path untuk generated QR codes
STORAGE_DIR = "storage/qris"


@view_config(route_name="payment_generate", request_method="POST", renderer="json")
@jwt_validate
def payment_generate(request):
    """
    POST /api/payment/generate
    Generate custom QRIS payment dengan amount (auto-fetch QRIS terbaru)
    
    Request (JSON):
    {
        "amount": 1000000
    }
    
    Response (200 OK):
    {
        "qris_id": "uuid-of-latest-qris",
        "static_qris_string": "00020126450014com.midtrans...",
        "dynamic_qris_string": "00020126...[custom amount]",
        "amount": 1000000,
        "fee_type": "rupiah",
        "fee_value": 10000,
        "total_amount": 1010000,
        "foto_qr_url": "http://localhost:6543/qris/dynamic_[uuid].png",
        "message": "Custom QRIS siap untuk diproses. Buka foto_qr_url atau scan untuk pembayaran."
    }
    """
    try:
        # Parse JSON body
        try:
            body = request.json_body
        except (ValueError, json.JSONDecodeError):
            request.response.status = 400
            return {"error": "Invalid JSON body"}
        
        amount = body.get("amount")
        
        if not amount:
            request.response.status = 400
            return {"error": "amount is required"}
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("amount must be > 0")
        except (ValueError, TypeError):
            request.response.status = 400
            return {"error": "amount must be a valid number > 0"}
        
        # Get latest QRIS from database (order by created_at descending)
        db_session = request.dbsession
        query = select(Qris).order_by(desc(Qris.created_at)).limit(1)
        result = db_session.execute(query)
        qris = result.scalar_one_or_none()
        
        if not qris:
            request.response.status = 404
            return {"error": "QRIS not found. Silakan upload QRIS terlebih dahulu."}
        
        # Generate dynamic QRIS string dengan amount dan fee
        dynamic_qris_string = generate_dynamic_qris_string(
            qris.static_qris_string,
            amount,
            qris.fee_type,
            qris.fee_value
        )
        
        # Generate QR code image dari dynamic QRIS string
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(dynamic_qris_string)
        qr.make(fit=True)
        
        # Create PIL image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save generated QR code to storage
        os.makedirs(STORAGE_DIR, exist_ok=True)
        dynamic_qr_filename = f"dynamic_{uuid.uuid4()}.png"
        dynamic_qr_path = os.path.join(STORAGE_DIR, dynamic_qr_filename)
        img.save(dynamic_qr_path)
        
        # Calculate total amount with fee
        total_amount = amount
        if qris.fee_type == "rupiah" and qris.fee_value:
            total_amount += float(qris.fee_value)
        elif qris.fee_type == "persentase" and qris.fee_value:
            total_amount += (amount * float(qris.fee_value) / 100)
        
        # Generate accessible URL untuk generated QR code
        dynamic_qr_url = f"{request.host_url.rstrip('/')}/qris/{dynamic_qr_filename}"
        
        return {
            "qris_id": str(qris.id),
            "static_qris_string": qris.static_qris_string,
            "dynamic_qris_string": dynamic_qris_string,
            "amount": amount,
            "fee_type": qris.fee_type,
            "fee_value": float(qris.fee_value) if qris.fee_value else None,
            "total_amount": total_amount,
            "foto_qr_url": dynamic_qr_url,
            "qr_code_image": dynamic_qr_path,
            "created_at": qris.created_at.isoformat() if qris.created_at else None,
            "message": "Custom QRIS berhasil di-generate. Buka foto_qr_url untuk QR code payment custom."
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
