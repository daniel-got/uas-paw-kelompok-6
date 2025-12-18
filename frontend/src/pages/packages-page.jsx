import { useEffect, useState, useMemo } from "react";
import { Search, Phone, Loader2, Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { PackageCardSkeleton } from "@/components/ui/skeleton";
import MainLayout from "@/layout/main-layout";
import { useDestinationStore } from "@/store/destination-store";
import { useWishlistStore } from "@/store/wishlist-store";
import { useAuthStore } from "@/store/auth-store";
import * as packageService from "@/services/package.service";
import * as destinationService from "@/services/destination.service";
import { useSEO } from "@/hooks/use-seo";
import { useDebounce } from "@/hooks/use-debounce";
import { useUrlParams } from "@/hooks/use-url-params";
import { toast } from "sonner";
import { getImageUrl } from "@/lib/image-utils";
import { getWhatsAppLink } from "@/lib/formatters";

export default function PackagesPage() {
  const navigate = useNavigate();
  const { destinations, packages, setDestinations, setPackages } = useDestinationStore();
  const { addToWishlist, removeFromWishlist, isInWishlist } = useWishlistStore();
  const { isAuthenticated } = useAuthStore();
  const { getParam, setParams } = useUrlParams();

  const [searchQuery, setSearchQuery] = useState(getParam("search", ""));
  const [selectedDestination, setSelectedDestination] = useState(getParam("destination", "all"));
  const [priceRange, setPriceRange] = useState(getParam("price", "all"));
  const [sortBy, setSortBy] = useState(getParam("sort", "popular"));
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 9;

  // Debounce search query
  const debouncedSearch = useDebounce(searchQuery, 500);

  useSEO({
    title: "Travel Packages",
    description:
      "Explore our collection of amazing travel packages to destinations worldwide. Find your perfect vacation with Wonderfull Inn.",
    keywords:
      "travel packages, vacation deals, holiday packages, tour packages, travel destinations",
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
      } catch (err) {
        console.error("Failed to fetch data:", err);
        toast.error("Failed to load packages");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Update URL params when filters change
  useEffect(() => {
    setParams({
      search: debouncedSearch,
      destination: selectedDestination === "all" ? "" : selectedDestination,
      price: priceRange === "all" ? "" : priceRange,
      sort: sortBy === "popular" ? "" : sortBy,
    });
  }, [debouncedSearch, selectedDestination, priceRange, sortBy, setParams]);

  // Reset to page 1 when filters change
  useEffect(() => {
    Promise.resolve().then(() => setCurrentPage(1));
  }, [debouncedSearch, selectedDestination, priceRange, sortBy]);

  const filteredPackages = useMemo(() => {
    let filtered = [...packages];

    if (debouncedSearch) {
      filtered = filtered.filter((pkg) =>
        pkg.name.toLowerCase().includes(debouncedSearch.toLowerCase())
      );
    }

    if (selectedDestination !== "all") {
      filtered = filtered.filter((pkg) => pkg.destinationId === selectedDestination);
    }

    // Price filtering
    if (priceRange !== "all") {
      const ranges = {
        "0-500": [0, 500],
        "500-1000": [500, 1000],
        "1000-2000": [1000, 2000],
        "2000+": [2000, Infinity],
      };
      const [min, max] = ranges[(priceRange, Infinity)];
      filtered = filtered.filter((pkg) => pkg.price >= min && pkg.price < max);
    }

    // Sorting
    switch (sortBy) {
      case "price-low":
        filtered.sort((a, b) => a.price - b.price);
        break;
      case "price-high":
        filtered.sort((a, b) => b.price - a.price);
        break;
      case "rating":
        filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        break;
      case "duration":
        filtered.sort((a, b) => a.duration - b.duration);
        break;
      default: // popular
        filtered.sort((a, b) => (b.reviewsCount || 0) - (a.reviewsCount || 0));
    }

    return filtered;
  }, [packages, debouncedSearch, selectedDestination, priceRange, sortBy]);

  const isSearching = searchQuery !== debouncedSearch;

  // Pagination
  const totalPages = Math.ceil(filteredPackages.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedPackages = filteredPackages.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const getDestinationById = (id) => {
    return destinations.find((d) => d.id === id);
  };

  const handleToggleWishlist = (e, packageId) => {
    e.stopPropagation();

    if (!isAuthenticated) {
      toast.error("Please sign in to add to wishlist");
      navigate("/sign-in");
      return;
    }

    if (isInWishlist(packageId)) {
      removeFromWishlist(packageId);
      toast.success("Removed from wishlist");
    } else {
      addToWishlist(packageId);
      toast.success("Added to wishlist");
    }
  };

  return (
    <MainLayout>
      <section className="space-y-8 py-2 md:py-8 lg:py-12">
        {/* Header */}
        <div className="space-y-4">
          <h1 className="text-foreground text-2xl font-bold md:text-4xl">
            Explore Travel Packages
          </h1>
          <p className="text-muted-foreground max-w-2xl text-sm md:text-lg">
            Discover amazing destinations and book your dream vacation package
          </p>
        </div>

        {/* Filters */}
        <div className="bg-card border-border rounded-lg border p-6">
          <div className="flex flex-col gap-4">
            {/* Search Bar */}
            <div className="space-y-2">
              <label className="text-muted-foreground text-sm font-medium">Search Packages</label>
              <div className="relative">
                <Search className="text-muted-foreground absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2" />
                <Input
                  placeholder="Search by package name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pr-10 pl-10"
                />
                {isSearching && (
                  <Loader2 className="text-muted-foreground absolute top-1/2 right-3 h-4 w-4 -translate-y-1/2 animate-spin" />
                )}
              </div>
            </div>

            {/* Filters Row */}
            <div className="flex flex-col gap-4 md:flex-row">
              <div className="flex-1 space-y-2">
                <label className="text-muted-foreground text-sm font-medium">Destination</label>
                <Select value={selectedDestination} onValueChange={setSelectedDestination}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Destinations</SelectItem>
                    {destinations.map((dest) => (
                      <SelectItem key={dest.id} value={dest.id}>
                        {dest.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="flex-1 space-y-2">
                <label className="text-muted-foreground text-sm font-medium">Price Range</label>
                <Select value={priceRange} onValueChange={setPriceRange}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Prices</SelectItem>
                    <SelectItem value="0-500">$0 - $500</SelectItem>
                    <SelectItem value="500-1000">$500 - $1,000</SelectItem>
                    <SelectItem value="1000-2000">$1,000 - $2,000</SelectItem>
                    <SelectItem value="2000+">$2,000+</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex-1 space-y-2">
                <label className="text-muted-foreground text-sm font-medium">Sort By</label>
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="popular">Most Popular</SelectItem>
                    <SelectItem value="rating">Highest Rated</SelectItem>
                    <SelectItem value="price-low">Price: Low to High</SelectItem>
                    <SelectItem value="price-high">Price: High to Low</SelectItem>
                    <SelectItem value="duration">Duration</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="flex items-center justify-between">
          <p className="text-muted-foreground text-sm">
            Showing {startIndex + 1}-{Math.min(endIndex, filteredPackages.length)} of{" "}
            {filteredPackages.length} packages
          </p>
          {totalPages > 1 && (
            <p className="text-muted-foreground text-sm">
              Page {currentPage} of {totalPages}
            </p>
          )}
        </div>

        {/* Package Grid */}
        {isLoading ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <PackageCardSkeleton key={i} />
            ))}
          </div>
        ) : filteredPackages.length > 0 ? (
          <>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {paginatedPackages.map((pkg) => {
                const destination = getDestinationById(pkg.destinationId);
                return (
                  <Card
                    key={pkg.id}
                    className="border-border group cursor-pointer overflow-hidden p-2 transition-shadow hover:shadow-lg"
                    onClick={() => navigate(`/packages/${pkg.id}`)}
                  >
                    <div className="relative">
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
                      
                      {/* Wishlist Button */}
                      <Button
                        variant="outline"
                        size="icon"
                        className={`bg-background/90 hover:bg-background absolute top-4 right-4 h-8 w-8 rounded-full ${
                          isInWishlist(pkg.id) ? "border-red-500 text-red-500" : ""
                        }`}
                        onClick={(e) => handleToggleWishlist(e, pkg.id)}
                      >
                        <Heart
                          className={`h-4 w-4 ${isInWishlist(pkg.id) ? "fill-current" : ""}`}
                        />
                      </Button>
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
                          {pkg.contactPhone && (
                            <a
                              href={getWhatsAppLink(pkg.contactPhone)}
                              target="_blank"
                              rel="noopener noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="text-primary mt-1 flex items-center gap-1 text-xs hover:underline"
                            >
                              <Phone className="h-3 w-3" />
                              <span>{pkg.contactPhone}</span>
                            </a>
                          )}
                        </div>

                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">
                            {pkg.duration} {pkg.duration === 1 ? "Day" : "Days"}
                          </span>
                         
                        </div>

                        <Button className="bg-primary text-primary-foreground hover:bg-primary/90 w-full">
                          View Details
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 pt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>

                <div className="flex gap-1">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                    // Show first page, last page, current page, and pages around current
                    if (
                      page === 1 ||
                      page === totalPages ||
                      (page >= currentPage - 1 && page <= currentPage + 1)
                    ) {
                      return (
                        <Button
                          key={page}
                          variant={currentPage === page ? "default" : "outline"}
                          size="sm"
                          onClick={() => handlePageChange(page)}
                          className="min-w-10"
                        >
                          {page}
                        </Button>
                      );
                    } else if (page === currentPage - 2 || page === currentPage + 2) {
                      return (
                        <span key={page} className="px-2">
                          ...
                        </span>
                      );
                    }
                    return null;
                  })}
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        ) : (
          <Card className="border-border p-12 text-center">
            <p className="text-muted-foreground">
              No packages found. Try adjusting your search filters.
            </p>
          </Card>
        )}
      </section>
    </MainLayout>
  );
}
