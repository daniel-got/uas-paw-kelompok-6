import apiClient from "./api";
// Get all reviews for a package
export const getPackageReviews = async (packageId) => {
  const response = await apiClient.get(`/api/reviews/package/${packageId}`);
  
 
  return response.data.data || response.data || [];
};


// Get reviews by tourist
export const getReviewsByTourist = async (touristId) => {
  const response = await apiClient.get(`/api/reviews/tourist/${touristId}`);
  return response.data.data; 
};

// Create review (Tourist only, after completing trip)
export const createReview = async (data) => {
  const response = await apiClient.post("/api/reviews", data);
  return response.data;
};

// Helper: Calculate average rating from reviews array (client-side)
export const calculatePackageRating = (reviews) => {
  if (reviews.length === 0) {
    return { average: 0, count: 0 };
  }
  const total = reviews.reduce((sum, review) => sum + review.rating, 0);
  return {
    average: Math.round((total / reviews.length) * 10) / 10,
    count: reviews.length,
  };
};
