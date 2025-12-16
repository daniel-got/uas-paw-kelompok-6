import axios from "axios";
import { logger } from "@/lib/logger";
import { toast } from "sonner";
import { getAuthToken, clearAuthStorage } from "@/lib/auth-storage";
import { API_BASE_URL, API_TIMEOUT } from "@/lib/constants";

// Re-export for backward compatibility
export { API_BASE_URL };

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: API_TIMEOUT,
});

// Request interceptor - add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    // Get token from helper
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      switch (status) {
        case 401:
          // Unauthorized - clear all auth data and redirect to login
          // Only redirect if not already on sign-in page to prevent loops
          if (!window.location.pathname.includes("/sign-in")) {
            clearAuthStorage();
            toast.error("Session expired. Please login again.");
            window.location.href = "/sign-in";
          }
          break;
        case 403:
          // Forbidden
          logger.error("Access forbidden:", data.message);
          toast.error("Access forbidden");
          break;
        case 404:
          // Not found
          logger.error("Resource not found:", data.message);
          toast.error("Resource not found");
          break;
        case 500:
        case 502:
        case 503:
        case 504:
          // Server error - don't redirect, just show error
          logger.error("Server error:", data?.message || "Server unavailable");
          toast.error("Server error. Please try again later.");
          break;
        default:
          logger.error("API Error:", data?.message);
          toast.error(data?.message || "An error occurred");
      }
    } else if (error.request) {
      // Request made but no response (network error or server down)
      logger.error("Network error: No response from server");
      toast.error("Cannot connect to server. Please check if the backend is running.");
    } else {
      // Error in request setup
      logger.error("Error:", error.message);
      toast.error("An unexpected error occurred");
    }

    return Promise.reject(error);
  }
);

export default apiClient;
