import apiClient from "./api";

// Get all bookings (Admin/Agent)
export const getAllBookings = async () => {
  try {
    const response = await apiClient.get("/api/bookings");
    console.log('getAllBookings response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching all bookings:', error);
    return [];
  }
};

// Get booking by ID
export const getBookingById = async (id) => {
  try {
    const response = await apiClient.get(`/api/bookings/${id}`);
    console.log('getBookingById response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error fetching booking by ID:', error);
    throw error;
  }
};

// Get bookings by tourist
export const getBookingsByTourist = async (touristId) => {
  try {
    const response = await apiClient.get(`/api/bookings/tourist/${touristId}`);
    console.log('getBookingsByTourist response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching bookings by tourist:', error);
    return [];
  }
};

// Get bookings by package
export const getBookingsByPackage = async (packageId) => {
  try {
    const response = await apiClient.get(`/api/bookings/package/${packageId}`);
    console.log('getBookingsByPackage response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching bookings by package:', error);
    return [];
  }
};

// Create booking (Tourist only)
export const createBooking = async (data) => {
  try {
    const response = await apiClient.post("/api/bookings", data);
    console.log('createBooking response:', response);
    
    // Handle different response structures
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error creating booking:', error);
    throw error;
  }
};

// Update booking status (Agent only)
export const updateBookingStatus = async (data) => {
  try {
    const { id, status } = data;
    const response = await apiClient.put(`/api/bookings/${id}/status`, { status });
    console.log('updateBookingStatus response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error updating booking status:', error);
    throw error;
  }
};

// Cancel booking (Tourist can cancel their own)
export const cancelBooking = async (id) => {
  try {
    const response = await apiClient.put(`/api/bookings/${id}/status`, {
      status: "cancelled",
    });
    console.log('cancelBooking response:', response);
    
    if (response.data?.data) {
      return response.data.data;
    }
    if (response.data) {
      return response.data;
    }
    return null;
  } catch (error) {
    console.error('Error cancelling booking:', error);
    throw error;
  }
};

// Get pending payment bookings (Agent only)
export const getPendingPaymentBookings = async () => {
  try {
    const response = await apiClient.get("/api/bookings/payment/pending");
    console.log('getPendingPaymentBookings response:', response);
    
    if (response.data?.data && Array.isArray(response.data.data)) {
      return response.data.data;
    }
    if (Array.isArray(response.data)) {
      return response.data;
    }
    return [];
  } catch (error) {
    console.error('Error fetching pending payment bookings:', error);
    return [];
  }
};