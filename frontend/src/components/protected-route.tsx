import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "@/store/auth-store";
import { Spinner } from "@/components/ui/spinner";
import { hasAuthToken } from "@/lib/auth-storage";

interface ProtectedRouteProps {
    children: React.ReactNode;
    allowedRoles?: ("tourist" | "agent")[];
}

export function ProtectedRoute({
    children,
    allowedRoles,
}: ProtectedRouteProps) {
    const { user, isAuthenticated, isLoading } = useAuthStore();
    const location = useLocation();

    // Show loading state while checking auth
    if (isLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <Spinner className="h-8 w-8" />
            </div>
        );
    }

    // Check if user has token and is authenticated
    const hasToken = hasAuthToken();

    // If no token or not authenticated, redirect to sign-in
    if (!hasToken || !isAuthenticated) {
        return <Navigate to="/sign-in" state={{ from: location }} replace />;
    }

    // If user doesn't exist (shouldn't happen but safety check)
    if (!user) {
        return <Navigate to="/sign-in" state={{ from: location }} replace />;
    }

    // If specific roles are required, check if user has permission
    if (allowedRoles && !allowedRoles.includes(user.role)) {
        return <Navigate to="/dashboard" replace />;
    }

    return <>{children}</>;
}
