import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";
import { useAuthStore } from "@/store/auth-store";
import { ErrorBoundary } from "@/components/error-boundary";
import { RoutePreloader } from "@/components/route-preloader";
import { ProtectedRoute } from "@/components/protected-route";
import {
  PackagesPageSkeleton,
  DashboardPageSkeleton,
  DetailPageSkeleton,
  AuthPageSkeleton,
  GenericPageSkeleton,
} from "@/components/ui/skeleton";

// Eager load critical routes (landing page)
import LandingPage from "@/pages/landing-page";

// Lazy load all other pages
const PackagesPage = lazy(() => import("@/pages/packages-page"));
const DestinationsPage = lazy(() => import("@/pages/destinations-page"));
const PackageDetailPage = lazy(() => import("@/pages/package-detail-page"));
const BookingPage = lazy(() => import("@/pages/booking-page"));
const BookingSuccessPage = lazy(() => import("@/pages/booking-success-page"));
const AllBookingsPage = lazy(() => import("@/pages/all-bookings-page"));
const ManagePackagesPage = lazy(() => import("@/pages/manage-packages-page"));
const CreatePackagePage = lazy(() => import("@/pages/create-package-page"));
const EditPackagePage = lazy(() => import("@/pages/edit-package-page"));
const AboutPage = lazy(() => import("@/pages/about-page"));
const ContactPage = lazy(() => import("@/pages/contact-page"));
const HelpPage = lazy(() => import("@/pages/help-page"));
const ProfilePage = lazy(() => import("@/pages/profile-page"));
const WishlistPage = lazy(() => import("@/pages/wishlist-page"));
const NotFoundPage = lazy(() => import("@/pages/not-found-page"));
const TouristDashboard = lazy(() => import("@/pages/dashboard/tourist-dashboard"));
const AgentDashboard = lazy(() => import("@/pages/dashboard/agent-dashboard"));
const SignIn = lazy(() => import("@/pages/auth/sign-in").then((m) => ({ default: m.SignIn })));
const SignUp = lazy(() => import("@/pages/auth/sign-up").then((m) => ({ default: m.SignUp })));

function DashboardRouter() {
  const { user } = useAuthStore();

  if (user?.role === "agent") {
    return <AgentDashboard />;
  }

  return <TouristDashboard />;
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <RoutePreloader />
        <Toaster richColors position="top-right" />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/packages"
            element={
              <Suspense fallback={<PackagesPageSkeleton />}>
                <PackagesPage />
              </Suspense>
            }
          />
          <Route
            path="/destinations"
            element={
              <Suspense fallback={<GenericPageSkeleton />}>
                <DestinationsPage />
              </Suspense>
            }
          />
          <Route
            path="/packages/:id"
            element={
              <Suspense fallback={<DetailPageSkeleton />}>
                <PackageDetailPage />
              </Suspense>
            }
          />
          <Route
            path="/about"
            element={
              <Suspense fallback={<GenericPageSkeleton />}>
                <AboutPage />
              </Suspense>
            }
          />
          <Route
            path="/contact"
            element={
              <Suspense fallback={<GenericPageSkeleton />}>
                <ContactPage />
              </Suspense>
            }
          />
          <Route
            path="/help"
            element={
              <Suspense fallback={<GenericPageSkeleton />}>
                <HelpPage />
              </Suspense>
            }
          />

          {/* Auth */}
          <Route
            path="/sign-in"
            element={
              <Suspense fallback={<AuthPageSkeleton />}>
                <SignIn />
              </Suspense>
            }
          />
          <Route
            path="/sign-up"
            element={
              <Suspense fallback={<AuthPageSkeleton />}>
                <SignUp />
              </Suspense>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/book/:id"
            element={
              <ProtectedRoute>
                <Suspense fallback={<DetailPageSkeleton />}>
                  <BookingPage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/booking-success"
            element={
              <ProtectedRoute>
                <Suspense fallback={<GenericPageSkeleton />}>
                  <BookingSuccessPage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/wishlist"
            element={
              <ProtectedRoute>
                <Suspense fallback={<PackagesPageSkeleton />}>
                  <WishlistPage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/all-bookings"
            element={
              <ProtectedRoute>
                <Suspense fallback={<DashboardPageSkeleton />}>
                  <AllBookingsPage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/manage-packages"
            element={
              <ProtectedRoute allowedRoles={["agent"]}>
                <Suspense fallback={<DashboardPageSkeleton />}>
                  <ManagePackagesPage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-package"
            element={
              <ProtectedRoute allowedRoles={["agent"]}>
                <Suspense fallback={<GenericPageSkeleton />}>
                  <CreatePackagePage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-package/:id"
            element={
              <ProtectedRoute allowedRoles={["agent"]}>
                <Suspense fallback={<GenericPageSkeleton />}>
                  <EditPackagePage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Suspense fallback={<DashboardPageSkeleton />}>
                  <DashboardRouter />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Suspense fallback={<GenericPageSkeleton />}>
                  <ProfilePage />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route
            path="/agent/dashboard"
            element={
              <ProtectedRoute allowedRoles={["agent"]}>
                <Suspense fallback={<DashboardPageSkeleton />}>
                  <AgentDashboard />
                </Suspense>
              </ProtectedRoute>
            }
          />

          {/* 404 */}
          <Route
            path="*"
            element={
              <Suspense fallback={<GenericPageSkeleton />}>
                <NotFoundPage />
              </Suspense>
            }
          />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
