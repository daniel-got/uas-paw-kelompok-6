import apiClient from "./api";
// Get all bookings (Admin/Agent) - Note: API returns {data: [...]}
export const getAllBookings = async () => {
  const response = await apiClient.get("/api/bookings");
  return response.data.data;
};

// Get booking by ID
export const getBookingById = async (id) => {
  const response = await apiClient.get(`/api/bookings/${id}`);
  return response.data.data;
};

// Get bookings by tourist
export const getBookingsByTourist = async (touristId) => {
  const response = await apiClient.get(`/api/bookings/tourist/${touristId}`);
  return response.data;
};

// Get bookings by package
export const getBookingsByPackage = async (packageId) => {
  const response = await apiClient.get(`/api/bookings/package/${packageId}`);
  return response.data;
};

// Create booking (Tourist only)
export const createBooking = async (data) => {
  const response = await apiClient.post("/api/bookings", data);
  return response.data;
};

// Update booking status (Agent only) - uses PUT method
export const updateBookingStatus = async (data) => {
  const { id, status } = data;
  const response = await apiClient.put(`/api/bookings/${id}/status`, {
    status,
  });
  return response.data;
};

// Cancel booking (Tourist can cancel their own) - uses PUT method
export const cancelBooking = async (id) => {
  const response = await apiClient.put(`/api/bookings/${id}/status`, {
    status: "cancelled",
  });
  return response.data;
};

// Get pending payment bookings (Agent only)
export const getPendingPaymentBookings = async () => {
  const response = await apiClient.get("/api/bookings/payment/pending");
  return response.data;
};
