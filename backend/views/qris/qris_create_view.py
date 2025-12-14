"""Upload QRIS image and save"""
import os
import uuid
from io import BytesIO
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from pyramid.view import view_config
from sqlalchemy import select

from models.qris_model import Qris
from helpers.jwt_validate_helper import jwt_validate


# Storage path configuration
STORAGE_DIR = "storage/qris"
ALLOWED_EXTENSIONS = {"jpeg", "png", "jpg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@view_config(route_name="qris", request_method="POST", renderer="json")
@jwt_validate
def qris_create(request):
    """
    POST /api/qris
    Upload QRIS image, auto-extract QRIS string, generate clean QR code
    
    Request (multipart/form-data):
    - foto_qr: file (required) - Image file berisi QR code (jpeg, png, jpg, gif)
    - fee_type: string (optional) - 'persentase' or 'rupiah'
    - fee_value: number (optional) - Fee value
    
    Response (201 Created):
    {
        "id": "uuid-here",
        "static_qris_string": "00020126450014com.midtrans...",
        "foto_qr_path": "storage/qris/qris_code.png",
        "fee_type": "rupiah",
        "fee_value": 10000,
        "created_at": "2024-01-01T00:00:00Z",
        "message": "QRIS berhasil diupload dan dibersihkan"
    }
    """
    try:
        # Validate file upload
        if "foto_qr" not in request.POST:
            request.response.status = 400
            return {"error": "foto_qr file is required"}
        
        foto_qr_file = request.POST["foto_qr"]
        
        # Validate file type
        allowed_types = ("image/jpeg", "image/png", "image/gif")
        content_type = getattr(foto_qr_file, 'content_type', '') or getattr(foto_qr_file, 'type', '')
        
        if content_type not in allowed_types:
            request.response.status = 400
            return {"error": f"foto_qr must be image file (jpeg, png, or gif). Got: {content_type}"}
        
        # Read file data
        image_data = foto_qr_file.file.read()
        file_size = len(image_data)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            request.response.status = 400
            return {"error": "foto_qr file size must be <= 5MB"}
        
        # Auto-extract QRIS string dari image
        image = Image.open(BytesIO(image_data))
        decoded_objects = decode(image)
        
        if not decoded_objects:
            request.response.status = 400
            return {"error": "Tidak dapat membaca QR code dari gambar. Pastikan gambar berisi QR code yang jelas."}
        
        # Ambil QRIS string dari QR code yang ter-decode
        static_qris_string = decoded_objects[0].data.decode('utf-8')
        
        if not static_qris_string:
            request.response.status = 400
            return {"error": "QR code tidak mengandung data."}
        
        # Validate fee params
        fee_type = request.POST.get("fee_type", "").strip() or None
        fee_value = request.POST.get("fee_value")
        
        if fee_type and fee_type not in ["persentase", "rupiah"]:
            request.response.status = 400
            return {"error": "fee_type must be 'persentase' or 'rupiah'"}
        
        if fee_value:
            try:
                fee_value = float(fee_value)
                if fee_value < 0:
                    raise ValueError("fee_value must be >= 0")
            except (ValueError, TypeError):
                request.response.status = 400
                return {"error": "fee_value must be a valid number"}
        
        # Check if QRIS string sudah ada
        db_session = request.dbsession
        existing_by_string = db_session.execute(
            select(Qris).where(Qris.static_qris_string == static_qris_string)
        ).scalar_one_or_none()
        
        if existing_by_string:
            request.response.status = 400
            return {"error": "QRIS string ini sudah pernah diupload sebelumnya."}
        
        # Create storage directory if not exists
        os.makedirs(STORAGE_DIR, exist_ok=True)
        
        # Delete existing files in storage directory (hanya 1 file yang disimpan)
        try:
            if os.path.exists(STORAGE_DIR):
                for filename in os.listdir(STORAGE_DIR):
                    file_to_delete = os.path.join(STORAGE_DIR, filename)
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)
        except Exception as e:
            print(f"Error deleting old files: {str(e)}")
        
        # Generate clean QR code dari QRIS string (tanpa file upload, hanya QR code bersih)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(static_qris_string)
        qr.make(fit=True)
        
        # Create clean PIL image dari QRIS string
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save clean QR code ke storage (tidak perlu nama unik, akan di-replace)
        clean_filename = "qris_code.png"
        file_path = os.path.join(STORAGE_DIR, clean_filename)
        img.save(file_path)
        
        # Save to database
        qris = Qris(
            foto_qr_path=file_path,
            static_qris_string=static_qris_string,
            dynamic_qris_string=static_qris_string,  # Akan di-update di payment generate
            fee_type=fee_type,
            fee_value=fee_value,
        )
        
        db_session.add(qris)
        db_session.flush()
        db_session.commit()
        
        request.response.status = 201
        return {
            "id": str(qris.id),
            "static_qris_string": qris.static_qris_string,
            "foto_qr_path": qris.foto_qr_path,
            "fee_type": qris.fee_type,
            "fee_value": float(qris.fee_value) if qris.fee_value else None,
            "created_at": qris.created_at.isoformat() if qris.created_at else None,
            "message": "QRIS berhasil diupload dan dibersihkan (disimpan sebagai clean QR code)"
        }
    
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
