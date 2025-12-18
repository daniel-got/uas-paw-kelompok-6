import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Calendar, MapPin, Star, Users, Phone, Heart, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import MainLayout from "@/layout/main-layout";
import { useDestinationStore } from "@/store/destination-store";
import { useAuthStore } from "@/store/auth-store";
import { useReviewStore } from "@/store/review-store";
import { useWishlistStore } from "@/store/wishlist-store";
import { ReviewCard } from "@/components/review-card";
import { ReviewForm } from "@/components/review-form";
import * as packageService from "@/services/package.service";
import * as destinationService from "@/services/destination.service";
import * as reviewService from "@/services/review.service";
import { useSEO } from "@/hooks/use-seo";
import { toast } from "sonner";
import { getImageUrl } from "@/lib/image-utils";
import { getWhatsAppLink } from "@/lib/formatters";


export default function PackageDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { destinations, setDestinations } = useDestinationStore();
  const { user, isAuthenticated } = useAuthStore();
  const { fetchReviewsByPackage, getReviewsByPackage } = useReviewStore();

 

  const { addToWishlist, removeFromWishlist, isInWishlist } = useWishlistStore();

  const [selectedImage, setSelectedImage] = useState(0);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [pkg, setPkg] = useState(null);
  const [destination, setDestination] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  const fetchData = async () => {
    if (!id) return;

    setIsLoading(true);
    try {
      const packageData = await packageService.getPackageById(id);
      setPkg(packageData);

      if (destinations.length === 0) {
        const destinationsData = await destinationService.getAllDestinations();
        setDestinations(destinationsData);
        setDestination(
          destinationsData.find(d => d.id === packageData.destinationId) || null
        );
      } else {
        setDestination(
          destinations.find(d => d.id === packageData.destinationId) || null
        );
      }

      // ✅ fetch reviews
      await fetchReviewsByPackage(id);

    } catch (err) {
      toast.error("Failed to load package details");
    } finally {
      setIsLoading(false);
    }
  };

  fetchData();
}, [id, destinations.length, fetchReviewsByPackage, setDestinations]);


  useSEO({
    title: pkg ? pkg.name : "Package Details",
    description: pkg
      ? `${pkg.itinerary.substring(0, 150)}... Explore this amazing package to ${destination?.name}.`
      : "View detailed information about this travel package",
    keywords: `${pkg?.name || "travel package"}, ${destination?.name || "destination"}, package details, travel itinerary`,
  });

  // Loading state
  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex min-h-[50vh] items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="text-primary h-8 w-8 animate-spin" />
            <p className="text-muted-foreground">Loading package details...</p>
          </div>
        </div>
      </MainLayout>
    );
  }

  if (!pkg || !destination) {
    return (
      <MainLayout>
        <div className="flex min-h-[50vh] items-center justify-center">
          <Card className="border-border p-8 text-center">
            <p className="text-muted-foreground">Package not found</p>
            <Button onClick={() => navigate("/packages")} className="mt-4" variant="outline">
              Back to Packages
            </Button>
          </Card>
        </div>
      </MainLayout>
    );
  }

  const handleBookNow = () => {
    if (!isAuthenticated) {
      navigate("/sign-in", { state: { from: `/packages/${id}` } });
    } else {
      navigate(`/book/${id}`);
    }
  };

  const handleToggleWishlist = () => {
    if (!isAuthenticated) {
      toast.error("Please sign in to add to wishlist");
      navigate("/sign-in", { state: { from: `/packages/${id}` } });
      return;
    }

    if (isInWishlist(id)) {
      removeFromWishlist(id);
      toast.success("Removed from wishlist");
    } else {
      addToWishlist(id);
      toast.success("Added to wishlist");
    }
  };

  return (
    <MainLayout>
      <section className="space-y-6 py-2 md:space-y-8 md:py-8 lg:py-12">
        {/* Back Button */}
        <Button variant="outline" onClick={() => navigate("/packages")} className="border-border">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Packages
        </Button>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Main Content */}
          <div className="space-y-6 lg:col-span-2">
            {/* Image Gallery */}
            <div className="space-y-4">
              <div className="border-border overflow-hidden rounded-lg border">
                <AspectRatio ratio={16 / 9}>
                  <img
                    src={getImageUrl(pkg.images[selectedImage])}
                    alt={pkg.name}
                    className="h-full w-full object-cover"
                  />
                </AspectRatio>
              </div>

              <div className="grid grid-cols-4 gap-4">
                {pkg.images.map((img, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedImage(idx)}
                    className={`border-border cursor-pointer overflow-hidden rounded-lg border transition-all ${
                      selectedImage === idx ? "ring-primary ring-2" : "hover:opacity-80"
                    }`}
                  >
                    <AspectRatio ratio={4 / 3}>
                      <img
                        src={getImageUrl(img)}
                        alt={`${pkg.name} view ${idx + 1}`}
                        className="h-full w-full object-cover"
                      />
                    </AspectRatio>
                  </div>
                ))}
              </div>
            </div>

            {/* Package Info */}
            <div className="space-y-6">
              <div>
                <div className="mb-2 flex items-start justify-between">
                  <div>
                    <h1 className="text-foreground text-3xl font-bold">{pkg.name}</h1>
                    <div className="text-muted-foreground mt-2 flex items-center gap-2 text-sm">
                      <MapPin className="h-4 w-4" />
                      <span>
                        {destination.name}, {destination.country}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={handleToggleWishlist}
                      className={isInWishlist(id) ? "border-red-500 text-red-500" : ""}
                    >
                      <Heart className={`h-4 w-4 ${isInWishlist(id) ? "fill-current" : ""}`} />
                    </Button>
                  </div>
                </div>

                <div className="mt-4 flex flex-wrap gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Calendar className="text-muted-foreground h-4 w-4" />
                    <span className="text-foreground">
                      {pkg.duration} {pkg.duration === 1 ? "Day" : "Days"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Users className="text-muted-foreground h-4 w-4" />
                    <span className="text-foreground">Max {pkg.maxTravelers} Travelers</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="text-muted-foreground h-4 w-4" />
                    <a
                      href={getWhatsAppLink(pkg.contactPhone)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary font-medium hover:underline"
                    >
                      {pkg.contactPhone}
                    </a>
                  </div>
                </div>
              </div>

              <Separator />

              {/* Tabs */}
              <Tabs defaultValue="description" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="description">Description</TabsTrigger>
                  <TabsTrigger value="itinerary">Itinerary</TabsTrigger>
                </TabsList>

                <TabsContent value="description" className="space-y-4 pt-4">
                  <div>
                    <h3 className="text-foreground mb-2 text-lg font-semibold">
                      About This Package
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {destination.description}
                    </p>
                  </div>
                </TabsContent>

                <TabsContent value="itinerary" className="space-y-4 pt-4">
                  <div>
                    <h3 className="text-foreground mb-3 text-lg font-semibold">
                      Day by Day Itinerary
                    </h3>
                    <div className="space-y-3">
                      {pkg.itinerary.split("|").map((day, idx) => (
                        <div key={idx} className="bg-muted/30 rounded-lg p-4">
                          <p className="text-foreground text-sm">{day.trim()}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </TabsContent>
              </Tabs>

              

              {/* Write Review Button */}
              {isAuthenticated && user?.role === "tourist" && (
                <Card className="border-border">
                  <CardContent className="pt-6">
                    <Button
                      onClick={() => setShowReviewForm(true)}
                      className="w-full"
                      variant="outline"
                    >
                      Write a Review
                    </Button>
                  </CardContent>
                </Card>
              )}

              {/* Reviews List */}
              <Card className="border-border">
  <CardHeader>
    <CardTitle className="text-foreground">
      Customer Reviews ({getReviewsByPackage(id || "").length})
    </CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    {getReviewsByPackage(id || "").length > 0 ? (
      getReviewsByPackage(id || "").map((review) => (
        <ReviewCard
          key={review.id}
          review={review}
          touristName={review.tourist?.name || "Anonymous Tourist"}
        />
      ))
    ) : (
      <div className="py-8 text-center">
        <p className="text-muted-foreground">
          No reviews yet. Be the first to review
        </p>
      </div>
    )}
  </CardContent>
</Card>

            </div>
          </div>

          {/* Booking Card - Sidebar on desktop, below images on mobile */}
          <div className="lg:col-span-1">
            <Card className="border-border lg:sticky lg:top-8">
              <CardHeader>
                <div className="flex items-baseline justify-between">
                  <div>
                    <p className="text-muted-foreground text-sm">Price per person</p>
                    <p className="text-foreground text-3xl font-bold">
                      ${pkg.price.toLocaleString()}
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-muted/30 space-y-3 rounded-lg p-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Duration</span>
                    <span className="text-foreground font-medium">{pkg.duration} days</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Max Travelers</span>
                    <span className="text-foreground font-medium">{pkg.maxTravelers} people</span>
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Contact</span>
                    <a
                      href={getWhatsAppLink(pkg.contactPhone)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary flex items-center gap-1 font-medium hover:underline"
                    >
                      <Phone className="h-3 w-3" />
                      {pkg.contactPhone}
                    </a>
                  </div>
                </div>

                <Button
                  onClick={handleBookNow}
                  className="bg-primary text-primary-foreground hover:bg-primary/90 w-full"
                  size="lg"
                >
                  Book Now
                </Button>

                <p className="text-muted-foreground text-center text-xs">
                  {!isAuthenticated && "Sign in required to book this package"}
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Review Form Dialog */}
        {pkg && (
          <ReviewForm
            packageId={pkg.id}
            packageName={pkg.name}
            open={showReviewForm}
            onOpenChange={setShowReviewForm}
          />
        )}
      </section>
    </MainLayout>
  );
}
