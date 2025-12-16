"use client";

import { useNavigate } from "react-router-dom";
import { Menu, LogOut, User, Heart } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";

import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";

interface MenuItem {
  title: string;
  url: string;
  description?: string;
  icon?: React.ReactNode;
  items?: MenuItem[];
}

interface Navbar1Props {
  logo?: {
    url: string;
    src: string;
    alt: string;
    title: string;
  };
  menu?: MenuItem[];
  auth?: {
    login: {
      title: string;
      url: string;
    };
    signup: {
      title: string;
      url: string;
    };
  };
}

const Navbar = ({
  logo = {
    url: "/",
    src: "/tree-palm.svg",
    alt: "logo",
    title: "Wanderlust Inn",
  },
  menu = [
    { title: "Home", url: "/" },
    { title: "Destinations", url: "/destinations" },
    { title: "Packages", url: "/packages" },
  ],
  auth = {
    login: { title: "Sign In", url: "/sign-in" },
    signup: { title: "Sign Up", url: "/sign-up" },
  },
}: Navbar1Props) => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate("/");
  };
  return (
    <section className="py-4">
      <div className="container">
        {/* Desktop Menu */}
        <nav className="hidden items-center justify-between lg:flex">
          <div className="flex items-center gap-6">
            {/* Logo */}
            <a href={logo.url} className="flex items-center gap-2">
              <img src={logo.src} className="max-h-8 dark:invert" alt={logo.alt} />
              <span className="text-lg font-semibold tracking-tighter">{logo.title}</span>
            </a>
            <div className="flex items-center gap-4">
              {menu.map((item) => (
                <Button key={item.title} variant="ghost" onClick={() => navigate(item.url)}>
                  {item.title}
                </Button>
              ))}
            </div>
          </div>
          <div className="flex gap-2">
            {isAuthenticated && user ? (
              <>
                <Button variant="outline" size="sm" onClick={() => navigate("/wishlist")}>
                  <Heart className="mr-2 h-4 w-4" />
                  Wishlist
                </Button>
                <Button variant="outline" size="sm" onClick={() => navigate("/dashboard")}>
                  <User className="mr-2 h-4 w-4" />
                  Dashboard
                </Button>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button variant="outline" size="sm" onClick={() => navigate(auth.login.url)}>
                  {auth.login.title}
                </Button>
                <Button size="sm" onClick={() => navigate(auth.signup.url)}>
                  {auth.signup.title}
                </Button>
              </>
            )}
          </div>
        </nav>

        {/* Mobile Menu */}
        <div className="block lg:hidden">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <a href={logo.url} className="flex items-center gap-2">
              <img src={logo.src} className="max-h-8 dark:invert" alt={logo.alt} />
            </a>
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon">
                  <Menu className="size-4" />
                </Button>
              </SheetTrigger>
              <SheetContent className="overflow-y-auto">
                <SheetHeader>
                  <SheetTitle>
                    <a href={logo.url} className="flex items-center gap-2">
                      <img src={logo.src} className="max-h-8 dark:invert" alt={logo.alt} />
                    </a>
                  </SheetTitle>
                </SheetHeader>
                <div className="flex flex-col gap-6 p-4">
                  <div className="flex flex-col gap-2">
                    {menu.map((item) => (
                      <Button
                        key={item.title}
                        variant="ghost"
                        className="justify-start"
                        onClick={() => navigate(item.url)}
                      >
                        {item.title}
                      </Button>
                    ))}
                  </div>

                  <div className="flex flex-col gap-3">
                    {isAuthenticated && user ? (
                      <>
                        <Button variant="outline" onClick={() => navigate("/wishlist")}>
                          <Heart className="mr-2 h-4 w-4" />
                          Wishlist
                        </Button>
                        <Button variant="outline" onClick={() => navigate("/dashboard")}>
                          <User className="mr-2 h-4 w-4" />
                          Dashboard
                        </Button>
                        <Button variant="ghost" onClick={handleLogout}>
                          <LogOut className="mr-2 h-4 w-4" />
                          Logout
                        </Button>
                      </>
                    ) : (
                      <>
                        <Button variant="outline" onClick={() => navigate(auth.login.url)}>
                          {auth.login.title}
                        </Button>
                        <Button onClick={() => navigate(auth.signup.url)}>
                          {auth.signup.title}
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </section>
  );
};

export { Navbar };
