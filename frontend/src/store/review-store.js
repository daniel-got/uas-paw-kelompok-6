import { create } from "zustand";
import * as reviewService from "@/services/review.service";

export const useReviewStore = create((set, get) => ({
  reviews: [],
  isLoading: false,
  error: null,

  setReviews: (reviews) => set({ reviews }),

  fetchReviewsByPackage: async (packageId) => {
  set({ isLoading: true, error: null });
  try {
    const rawReviews = await reviewService.getPackageReviews(packageId);
  
    const reviews = rawReviews.map((r) => ({
      ...r,
      packageId: r.package_id || r.packageId,
      touristId: r.tourist_id || r.touristId,
      // Map tourist object if it exists (handle both snake_case and camelCase)
      tourist: r.tourist || (r.tourist_name ? { name: r.tourist_name } : undefined),
    }));

    set((state) => {
      const existingIds = new Set(state.reviews.map((rev) => rev.id));
      const newReviews = reviews.filter((rev) => !existingIds.has(rev.id));

      return {
        reviews: [...state.reviews, ...newReviews],
        isLoading: false,
      };
    });
  } catch (error) {
    set({ error: error.message, isLoading: false });
  }
},

  fetchReviewsByTourist: async (touristId) => {
    set({ isLoading: true, error: null });
    try {
      const reviews = await reviewService.getReviewsByTourist(touristId);
      // Merge with existing reviews (avoid duplicates)
      set((state) => {
        const existingIds = new Set(state.reviews.map((r) => r.id));
        const newReviews = reviews.filter((r) => !existingIds.has(r.id));
        return {
          reviews: [...state.reviews, ...newReviews],
          isLoading: false,
        };
      });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  addReview: (review) =>
    set((state) => ({
      reviews: [...state.reviews, review],
    })),

  createReview: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const review = await reviewService.createReview(data);
      set((state) => ({
        reviews: [...state.reviews, review],
        isLoading: false,
      }));
      return review;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  getReviewsByPackage: (packageId) => {
    return get().reviews.filter((review) => review.packageId === packageId);
  },

  getReviewsByTourist: (touristId) => {
    return get().reviews.filter((review) => review.touristId === touristId);
  },

  getPackageAverageRating: (packageId) => {
    const packageReviews = get().reviews.filter((review) => review.packageId === packageId);
    return reviewService.calculatePackageRating(packageReviews);
  },

  hasUserReviewedPackage: (touristId, packageId) => {
    const reviews = get().reviews;
    return reviews.some(
      (review) => review.touristId === touristId && review.packageId === packageId
    );
  },
}));
