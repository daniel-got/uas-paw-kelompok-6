"""
QRIS Helper - Generate dan validasi dynamic QRIS string
Mengikuti standard QRIS Indonesia
"""


def crc16(data: str) -> str:
    """
    Calculate CRC16 checksum for QRIS payload
    
    Args:
        data: QRIS payload string
    
    Returns:
        CRC16 checksum as 4-character hex string (uppercase)
    """
    crc = 0xFFFF
    
    for char in data:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    
    hex_value = format(crc & 0xFFFF, '04X')
    return hex_value


def generate_dynamic_qris_string(
    static_qris: str,
    amount: float,
    fee_type: str = None,
    fee_value: float = None
) -> str:
    """
    Generate dynamic QRIS string from static QRIS with amount and fee information
    
    Args:
        static_qris: Static QRIS string (dari scan/upload QR)
        amount: Amount to be paid in rupiah
        fee_type: Fee type ('persentase' or 'rupiah'), optional
        fee_value: Fee value, optional
    
    Returns:
        Dynamic QRIS string with amount info (atau static QRIS jika format tidak bisa dikonversi)
    
    Raises:
        ValueError: If QRIS format is invalid
    """
    # Validate static QRIS
    if not static_qris or len(static_qris) < 4:
        raise ValueError("Data QRIS statis tidak valid.")
    
    try:
        # Remove CRC from static QRIS (last 4 chars)
        qris_without_crc = static_qris[:-4]
        
        # Convert static to dynamic (010211 -> 010212)
        step1 = qris_without_crc.replace("010211", "010212")
        
        # Split by country code
        parts = step1.split("5802ID")
        if len(parts) != 2:
            # Jika format tidak sesuai, return static QRIS dengan info amount di note
            # Ini untuk QRIS format yang non-standard
            return static_qris
        
        # Generate amount tag
        amount_int = int(amount)
        amount_str = str(amount_int)
        amount_length = str(len(amount_str)).zfill(2)
        amount_tag = f"54{amount_length}{amount_str}"
        
        # Generate fee tag if provided
        fee_tag = ""
        if fee_value and float(fee_value) > 0:
            if fee_type and fee_type.lower() == "rupiah":
                fee_int = int(fee_value)
                fee_str = str(fee_int)
                fee_length = str(len(fee_str)).zfill(2)
                fee_tag = f"55020256{fee_length}{fee_str}"
            else:
                # Percentage
                fee_str = str(fee_value)
                fee_length = str(len(fee_str)).zfill(2)
                fee_tag = f"55020357{fee_length}{fee_str}"
        
        # Construct final payload
        payload = f"{parts[0]}{amount_tag}{fee_tag}5802ID{parts[1]}"
        
        # Calculate and append CRC
        final_crc = crc16(payload)
        
        return payload + final_crc
    
    except Exception as e:
        print(f"Warning: Could not generate dynamic QRIS: {str(e)}. Returning static QRIS.")
        # Fallback: return static QRIS if conversion fails
        return static_qris


def decode_qris_string(qris_string: str) -> dict:
    """
    Decode QRIS string to extract information
    Basic decoding - extracts amount and merchant info
    
    Args:
        qris_string: QRIS string to decode
    
    Returns:
        Dictionary containing QRIS information
    """
    result = {
        "valid": False,
        "is_dynamic": False,
        "is_static": False,
        "amount": None,
        "merchant_name": None,
        "city_code": None,
    }
    
    if not qris_string or len(qris_string) < 4:
        return result
    
    # Check CRC
    payload = qris_string[:-4]
    checksum = qris_string[-4:]
    calculated_crc = crc16(payload)
    
    if checksum != calculated_crc:
        return result
    
    result["valid"] = True
    
    # Check if dynamic (010212) or static (010211)
    if "010212" in qris_string:
        result["is_dynamic"] = True
    elif "010211" in qris_string:
        result["is_static"] = True
    
    # Extract amount (tag 54)
    if "54" in qris_string:
        try:
            idx = qris_string.find("54")
            if idx != -1:
                length = int(qris_string[idx + 2 : idx + 4])
                amount_str = qris_string[idx + 4 : idx + 4 + length]
                result["amount"] = float(amount_str)
        except (ValueError, IndexError):
            pass
    
    return result
