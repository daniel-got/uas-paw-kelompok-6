import apiClient from "./api";

// Get all QRIS records (Agent only)
export const getAllQRIS = async () => {
  try {
    const response = await apiClient.get("/api/qris");
    console.log('getAllQRIS response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching all QRIS:', error);
    return [];
  }
};

// Get QRIS by ID (Agent only)
export const getQRISById = async (id) => {
  try {
    const response = await apiClient.get(`/api/qris/${id}`);
    console.log('getQRISById response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error fetching QRIS by ID:', error);
    throw error;
  }
};

// Create/Upload new QRIS (Agent only)
export const createQRIS = async (file, feeType, feeValue) => {
  try {
    const formData = new FormData();
    formData.append("foto_qr", file);

    if (feeType) {
      formData.append("fee_type", feeType);
    }
    if (feeValue !== undefined) {
      formData.append("fee_value", feeValue.toString());
    }

    const response = await apiClient.post("/api/qris", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    
    console.log('createQRIS response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error creating QRIS:', error);
    throw error;
  }
};

// Delete QRIS by ID (Agent only)
export const deleteQRIS = async (id) => {
  try {
    const response = await apiClient.delete(`/api/qris/${id}`);
    console.log('deleteQRIS response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error deleting QRIS:', error);
    throw error;
  }
};

// Preview QRIS with amount (no auth required)
export const previewQRIS = async (qrisId, amount) => {
  try {
    const response = await apiClient.post("/api/qris/preview", {
      qrisId,
      amount,
    });
    
    console.log('previewQRIS response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error previewing QRIS:', error);
    throw error;
  }
};

// Generate payment QRIS with amount (Tourist/Agent)
export const generatePaymentQRIS = async (amount) => {
  try {
    const response = await apiClient.post("/api/payment/generate", {
      amount,
    });
    
    console.log('generatePaymentQRIS response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error generating payment QRIS:', error);
    throw error;
  }
};