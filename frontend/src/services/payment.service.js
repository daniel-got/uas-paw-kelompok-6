import apiClient from "./api";

// Upload payment proof (Tourist)
export const uploadPaymentProof = async (bookingId, file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post(
      `/api/bookings/${bookingId}/payment-proof`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    
    console.log('uploadPaymentProof response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error uploading payment proof:', error);
    throw error;
  }
};

// Verify payment (Agent only)
export const verifyPayment = async (bookingId) => {
  try {
    const response = await apiClient.put(`/api/bookings/${bookingId}/payment-verify`);
    console.log('verifyPayment response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error verifying payment:', error);
    throw error;
  }
};

// Reject payment (Agent only)
export const rejectPayment = async (bookingId, reason) => {
  try {
    const response = await apiClient.put(
      `/api/bookings/${bookingId}/payment-reject`,
      { reason }
    );
    console.log('rejectPayment response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error rejecting payment:', error);
    throw error;
  }
};

// Get pending payments (Agent only)
export const getPendingPayments = async () => {
  try {
    const response = await apiClient.get("/api/bookings/payment/pending");
    console.log('getPendingPayments response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching pending payments:', error);
    return [];
  }
};

// Generate QRIS for payment (deprecated - use qris.service.js instead)
export const generateQRIS = async (data) => {
  try {
    const response = await apiClient.post("/api/payment/generate", data);
    console.log('generateQRIS response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error generating QRIS:', error);
    throw error;
  }
};