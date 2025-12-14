"""Generate preview of dynamic QRIS without saving"""
import base64
import io
import json
from pyramid.view import view_config
import qrcode

from helpers.qris_helper import generate_dynamic_qris_string
from helpers.jwt_validate_helper import jwt_validate


@view_config(route_name="qris_preview", request_method="POST", renderer="json")
@jwt_validate
def qris_preview(request):
    """
    POST /api/qris/preview
    Generate preview of dynamic QRIS QR code without saving to database
    
    Request (JSON):
    {
        "static_qris_string": "00020126450014com.midtrans...",
        "jumlah_bayar": 1000000,
        "fee_type": "rupiah",
        "fee_value": 10000
    }
    
    Response (200 OK):
    {
        "base64_qr": "iVBORw0KGgoAAAANSUhEUgAA...",
        "dynamic_qris_string": "00020126..."
    }
    """
    try:
        # Parse JSON body
        try:
            body = request.json_body
        except (ValueError, json.JSONDecodeError):
            request.response.status = 400
            return {"error": "Invalid JSON body"}
        
        # Validate required fields
        static_qris_string = body.get("static_qris_string", "").strip()
        jumlah_bayar = body.get("jumlah_bayar")
        fee_type = body.get("fee_type", "").strip() or None
        fee_value = body.get("fee_value")
        
        if not static_qris_string:
            request.response.status = 400
            return {"error": "static_qris_string is required"}
        
        if jumlah_bayar is None:
            request.response.status = 400
            return {"error": "jumlah_bayar is required"}
        
        # Parse numeric values
        try:
            jumlah_bayar = float(jumlah_bayar)
            if jumlah_bayar < 0:
                raise ValueError("jumlah_bayar must be >= 0")
        except (ValueError, TypeError):
            request.response.status = 400
            return {"error": "jumlah_bayar must be a valid number"}
        
        if fee_value is not None:
            try:
                fee_value = float(fee_value)
                if fee_value < 0:
                    raise ValueError("fee_value must be >= 0")
            except (ValueError, TypeError):
                request.response.status = 400
                return {"error": "fee_value must be a valid number"}
        
        if fee_type and fee_type not in ["persentase", "rupiah"]:
            request.response.status = 400
            return {"error": "fee_type must be 'persentase' or 'rupiah'"}
        
        # Generate dynamic QRIS string
        try:
            dynamic_qris_string = generate_dynamic_qris_string(
                static_qris_string,
                jumlah_bayar,
                fee_type,
                fee_value
            )
        except ValueError as e:
            request.response.status = 400
            return {"error": str(e)}
        
        # Generate QR code
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(dynamic_qris_string)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)
            
            base64_qr = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
        except Exception as e:
            request.response.status = 400
            return {"error": f"Failed to generate QR code: {str(e)}"}
        
        return {
            "base64_qr": base64_qr,
            "dynamic_qris_string": dynamic_qris_string,
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
