import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { BookingSearch } from "@/components/booking-search";
import { FeaturedPackages } from "@/components/featured-packages";
import { AboutSection } from "@/components/about-section";
import { PromoSection } from "@/components/promo-section";
import { NewsletterSection } from "@/components/newsletter-section";
import MainLayout from "@/layout/main-layout";
import { useDestinationStore } from "@/store/destination-store";
import * as packageService from "@/services/package.service";
import * as destinationService from "@/services/destination.service";
import { useSEO } from "@/hooks/use-seo";
import { Loader2 } from "lucide-react";

const heroImage =
  "https://images.unsplash.com/photo-1540202404-a2f29016b523?q=80&w=2000&auto=format&fit=crop";

export default function LandingPage() {
  const navigate = useNavigate();
  const { destinations, packages, setDestinations, setPackages } = useDestinationStore();
  const [isLoading, setIsLoading] = useState(true);

  useSEO({
    title: "Home",
    description:
      "Discover amazing travel packages and book your dream vacation with Wonderfull Inn. Explore destinations worldwide with expert travel agents.",
    keywords:
      "travel packages, vacation booking, holiday destinations, tourism, travel agent, Wonderfull Inn",
    ogImage: heroImage,
  });

  useEffect(() => {
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
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex min-h-[50vh] items-center justify-center">
          <Loader2 className="text-primary h-8 w-8 animate-spin" />
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <section className="space-y-12 py-8 lg:py-16">
        {/* Hero Section */}
        <div className="space-y-6">
          {/* Hero Header */}
          <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
            <div className="space-y-2 md:space-y-4">
              <h1 className="text-foreground text-2xl leading-tight font-bold md:text-4xl lg:text-5xl">
                Refresh, Relax, and Rediscover
                <br />
                Life's Simple Pleasures
              </h1>
              <p className="text-muted-foreground max-w-2xl text-base leading-relaxed md:text-lg">
                Discover the luxury, where tranquility meets the beauty of nature. Every moments
                feels like home with all the comfort of the luxurious inn.
              </p>
            </div>

            <div className="flex w-full flex-col gap-2 md:max-w-sm md:gap-3">
              <Button
                onClick={() => navigate("/packages")}
                className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full px-4 text-xs md:px-8 md:text-base"
              >
                Explore
              </Button>
              <Button
                onClick={() => navigate("/contact")}
                variant="outline"
                className="border-border rounded-full px-4 text-xs md:px-8 md:text-base"
              >
                Contact
              </Button>
            </div>
          </div>

          {/* Hero Image */}
          <div className="border-border overflow-hidden rounded-lg border">
            <img
              src={heroImage}
              alt="Luxury overwater villa with stunning ocean view"
              className="aspect-21/9 w-full object-cover"
            />
          </div>
        </div>

        {/* Booking Search */}
        <BookingSearch />

        {/* Featured Packages */}
        <FeaturedPackages packages={packages} destinations={destinations} />

        {/* About Section */}
        <AboutSection />

        {/* Promo Section */}
        <PromoSection />

        {/* Newsletter Section */}
        <NewsletterSection />
      </section>
    </MainLayout>
  );
}
