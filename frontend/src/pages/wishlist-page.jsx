import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Heart, Trash2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { Badge } from "@/components/ui/badge";
import MainLayout from "@/layout/main-layout";
import { useDestinationStore } from "@/store/destination-store";
import { useWishlistStore } from "@/store/wishlist-store";
import { useAuthStore } from "@/store/auth-store";
import * as packageService from "@/services/package.service";
import * as destinationService from "@/services/destination.service";
import { useSEO } from "@/hooks/use-seo";
import { toast } from "sonner";
import { getImageUrl } from "@/lib/image-utils";

export default function WishlistPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const { destinations, packages, setDestinations, setPackages } = useDestinationStore();
  const { wishlist, removeFromWishlist, clearWishlist } = useWishlistStore();
  const [isLoading, setIsLoading] = useState(true);

  useSEO({
    title: "My Wishlist",
    description: "View your saved travel packages and plan your future adventures",
    keywords: "wishlist, saved packages, favorites, travel planning",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/sign-in");
      return;
    }

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [packagesData, destinationsData] = await Promise.all([
          packageService.getAllPackages(),
          destinationService.getAllDestinations(),
        ]);
        setPackages(packagesData);
        setDestinations(destinationsData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
        toast.error("Failed to load packages");
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [isAuthenticated, navigate, setPackages, setDestinations]);

  const wishlistPackages = packages.filter((pkg) => wishlist.includes(pkg.id));

  const handleRemove = (packageId, packageName) => {
    removeFromWishlist(packageId);
    toast.success(`Removed "${packageName}" from wishlist`);
  };

  const handleClearAll = () => {
    if (window.confirm("Are you sure you want to clear your entire wishlist?")) {
      clearWishlist();
      toast.success("Wishlist cleared");
    }
  };

  return (
    <MainLayout>
      <section className="space-y-6 py-2 md:space-y-8 md:py-8 lg:py-12">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-foreground flex items-center gap-2 text-3xl font-bold md:text-4xl">
              
              My Wishlist
            </h1>
            <p className="text-muted-foreground mt-2 text-base md:text-lg">
              {wishlistPackages.length === 0
                ? "No packages saved yet"
                : `${wishlistPackages.length} ${wishlistPackages.length === 1 ? "package" : "packages"} saved`}
            </p>
          </div>
          {wishlistPackages.length > 0 && (
            <Button
              variant="outline"
              onClick={handleClearAll}
              className="text-destructive border-destructive hover:bg-destructive hover:text-destructive-foreground"
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Clear All
            </Button>
          )}
        </div>

        {/* Wishlist Grid */}
        {isLoading ? (
          <div className="flex min-h-[30vh] items-center justify-center">
            <Loader2 className="text-primary h-8 w-8 animate-spin" />
          </div>
        ) : wishlistPackages.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {wishlistPackages.map((pkg) => {
              const destination = destinations.find((d) => d.id === pkg.destinationId);
              return (
                <Card
                  key={pkg.id}
                  className="border-border group overflow-hidden p-2 transition-shadow hover:shadow-lg"
                >
                  <div
                    className="relative cursor-pointer"
                    onClick={() => navigate(`/packages/${pkg.id}`)}
                  >
                    <AspectRatio ratio={4 / 3}>
                      <img
                        src={getImageUrl(pkg.images[0])}
                        alt={pkg.name}
                        className="h-full w-full rounded-lg object-cover transition-all duration-500 ease-in-out"
                      />
                    </AspectRatio>
                    <div className="bg-background/90 absolute right-4 bottom-4 rounded-full px-4 py-2">
                      <span className="text-foreground text-sm font-bold">
                        ${pkg.price.toLocaleString()}
                      </span>
                    </div>
                    
                  </div>

                  <CardContent className="p-2">
                    <div className="space-y-4">
                      <div>
                        <h3 className="text-foreground line-clamp-1 text-lg font-bold">
                          {pkg.name}
                        </h3>
                        {destination && (
                          <p className="text-muted-foreground text-sm">
                            {destination.name}, {destination.country}
                          </p>
                        )}
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">
                          {pkg.duration} {pkg.duration === 1 ? "Day" : "Days"}
                        </span>
                        
                      </div>

                      <div className="flex gap-2">
                        <Button
                          className="bg-primary text-primary-foreground hover:bg-primary/90 flex-1"
                          onClick={() => navigate(`/book/${pkg.id}`)}
                        >
                          Book Now
                        </Button>
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => handleRemove(pkg.id, pkg.name)}
                          className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        ) : (
          <Card className="border-border p-12 text-center">
            <Heart className="text-muted-foreground mx-auto mb-4 h-16 w-16" />
            <h3 className="text-foreground mb-2 text-xl font-semibold">Your wishlist is empty</h3>
            <p className="text-muted-foreground mb-6">
              Start exploring packages and save your favorites here
            </p>
            <Button
              onClick={() => navigate("/packages")}
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              Explore Packages
            </Button>
          </Card>
        )}
      </section>
    </MainLayout>
  );
}
