import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuthStore } from "@/store/auth-store";
import { toast } from "sonner";
import { useSEO } from "@/hooks/use-seo";
import { saveAuthToken, hasAuthToken } from "@/lib/auth-storage";
import * as authService from "@/services/auth.service";

interface SignInProps {
  heading?: string;
  logo?: {
    url: string;
    src: string;
    alt: string;
    title?: string;
  };
  buttonText?: string;
  signupText?: string;
  signupUrl?: string;
}

const SignIn = ({
  heading = "Sign In to Wanderlust Inn",
  logo = {
    url: "/",
    src: "https://deifkwefumgah.cloudfront.net/shadcnblocks/block/block-1.svg",
    alt: "Wanderlust Inn",
    title: "Wanderlust Inn",
  },
  buttonText = "Sign In",
  signupText = "Don't have an account?",
  signupUrl = "/sign-up",
}: SignInProps) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Redirect if already authenticated with valid token
  useEffect(() => {
    if (isAuthenticated && hasAuthToken()) {
      // Redirect to the page they came from, or dashboard
      const from = (location.state as { from?: Location })?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  useSEO({
    title: "Sign In",
    description:
      "Sign in to your Wanderlust Inn account to manage your bookings and explore travel packages.",
    keywords: "sign in, login, account access, user authentication",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      toast.error("Please fill in all fields");
      return;
    }

    setIsSubmitting(true);

    try {
      // Backend determines role from database, not from login request
      const response = await authService.login({ email, password });

      // Check if login was successful (backend returns token and user)
      if (!response.token || !response.user) {
        toast.error("Invalid email or password");
        return;
      }

      // Store JWT token using helper
      saveAuthToken(response.token);

      // Update auth store with user data
      login(response.user);

      toast.success(`Welcome back, ${response.user.name}!`);

      // Redirect to the page they came from, or dashboard
      const from = (location.state as { from?: Location })?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    } catch (error: unknown) {
      // Error is already handled by API interceptor
      const err = error as { response?: { data?: { message?: string }; status?: number }; request?: unknown };

      // Only show specific error messages, API interceptor handles the rest
      if (err.response?.status === 401 && err.response?.data?.message) {
        toast.error(err.response.data.message);
      } else if (!err.response && err.request) {
        // Network error - backend is down
        toast.error("Cannot connect to server. Please ensure the backend is running.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="bg-muted min-h-screen">
      <div className="flex min-h-screen items-center justify-center px-4 py-8">
        <div className="flex w-full max-w-sm flex-col items-center gap-4 sm:max-w-md sm:gap-6">
          <a href={logo.url}>
            <img src={logo.src} alt={logo.alt} title={logo.title} className="h-8 sm:h-10 dark:invert" />
          </a>
          <form
            onSubmit={handleSubmit}
            className="border-muted bg-background flex w-full flex-col gap-y-3 rounded-lg border px-4 py-6 shadow-md sm:gap-y-4 sm:px-6 sm:py-8"
          >
            {heading && <h1 className="text-center text-lg font-semibold sm:text-xl">{heading}</h1>}

            <div className="space-y-1.5 sm:space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                className="text-sm"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="space-y-1.5 sm:space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                className="text-sm"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <Button type="submit" className="mt-2 w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <div className="flex items-center gap-2">
                  <Skeleton className="h-4 w-4 rounded-full" />
                  <span>Signing in...</span>
                </div>
              ) : (
                buttonText
              )}
            </Button>
          </form>
          <div className="text-muted-foreground flex justify-center gap-1 text-sm">
            <p>{signupText}</p>
            <a href={signupUrl} className="text-primary font-medium hover:underline">
              Sign up
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export { SignIn };
