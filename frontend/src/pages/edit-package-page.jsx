import { useEffect, useState, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import MainLayout from "@/layout/main-layout";
import { useAuthStore } from "@/store/auth-store";
import { packageSchema } from "@/lib/validations";
import { EditPackageForm } from "@/components/edit-package-form";
import { useFormValidation } from "@/hooks/use-form-validation";
import { useImageArray } from "@/hooks/use-image-array";
import { useSEO } from "@/hooks/use-seo";
import * as packageService from "@/services/package.service";
import * as destinationService from "@/services/destination.service";

export default function EditPackagePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuthStore();

  useSEO({
    title: "Edit Package",
    description: "Update your travel package details, pricing, and availability.",
    keywords: "edit package, update package, package management, agent tools",
  });

  // API data states
  const [isLoading, setIsLoading] = useState(true);
  const [pkg, setPkg] = useState(null);
  const [destinations, setDestinations] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    destinationId: "",
    duration: "",
    price: "",
    itinerary: "",
    maxTravelers: "",
    contactPhone: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const { errors, validate } = useFormValidation(packageSchema);
  const { images, resetImages: resetImagesOriginal, addImage, removeImage, updateImage } = useImageArray();

  const resetImages = useCallback(resetImagesOriginal, []);

  useEffect(() => {
    if (!isAuthenticated || user?.role !== "agent") {
      navigate("/sign-in");
      return;
    }

    if (!id) {
      setIsLoading(false);
      return;
    }

    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [packageData, destinationsData] = await Promise.all([
          packageService.getPackageById(id),
          destinationService.getAllDestinations(),
        ]);

        // Check permissions
        if (packageData.agentId !== user.id) {
          toast.error("You don't have permission to edit this package");
          navigate("/manage-packages");
          return;
        }

        setPkg(packageData);
        setDestinations(destinationsData);

        // Populate form
        setFormData({
          name: packageData.name,
          destinationId: packageData.destinationId,
          duration: packageData.duration.toString(),
          price: packageData.price.toString(),
          itinerary: packageData.itinerary,
          maxTravelers: packageData.maxTravelers.toString(),
          contactPhone: packageData.contactPhone || "",
        });
        resetImages(packageData.images.length > 0 ? packageData.images : [""]);
      } catch (error) {
        console.error("Failed to fetch package:", error);
        toast.error("Failed to load package");
        navigate("/manage-packages");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [isAuthenticated, user?.role, user?.id, navigate, id, resetImages]);

  const handleFieldChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const dataToValidate = {
      ...formData,
      duration: Number(formData.duration),
      price: Number(formData.price),
      maxTravelers: Number(formData.maxTravelers),
      images: images.filter((img) => img.trim() !== ""),
    };

    if (!validate(dataToValidate)) return;

    setIsSubmitting(true);

    try {
      await packageService.updatePackage(id, {
        name: dataToValidate.name,
        duration: dataToValidate.duration,
        price: dataToValidate.price,
        itinerary: dataToValidate.itinerary,
        maxTravelers: dataToValidate.maxTravelers,
        contactPhone: dataToValidate.contactPhone,
        images: dataToValidate.images,
      });

      toast.success("Package updated successfully!");
      navigate("/manage-packages");
    } catch (error) {
      console.error("Failed to update package:", error);
      toast.error("Failed to update package");
    } finally {
      setIsSubmitting(false);
    }
  };

  // Loading and not found states
  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex min-h-[50vh] items-center justify-center">
          <Loader2 className="text-primary h-8 w-8 animate-spin" />
        </div>
      </MainLayout>
    );
  }

  if (!pkg) {
    return (
      <MainLayout>
        <div className="flex min-h-[50vh] items-center justify-center">
          <Card className="border-border p-8 text-center">
            <p className="text-muted-foreground">Package not found</p>
            <Button onClick={() => navigate("/manage-packages")} className="mt-4" variant="outline">
              Back to Packages
            </Button>
          </Card>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <section className="space-y-6 py-2 md:space-y-8 md:py-8 lg:py-12">
        <div className="flex items-center justify-between">
          <div>
            <Button variant="ghost" onClick={() => navigate("/manage-packages")} className="mb-4">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Packages
            </Button>
            <h1 className="text-foreground text-3xl font-bold md:text-4xl">Edit Package</h1>
            <p className="text-muted-foreground mt-2">Update your travel package information</p>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <Card className="border-border">
                <CardHeader>
                  <CardTitle>Package Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <EditPackageForm
                    formData={formData}
                    images={images}
                    errors={errors}
                    destinations={destinations}
                    onFieldChange={handleFieldChange}
                    onImageAdd={addImage}
                    onImageRemove={removeImage}
                    onImageChange={updateImage}
                  />
                </CardContent>
              </Card>
            </div>

            <div className="lg:col-span-1">
              <Card className="border-border sticky top-8">
                <CardHeader>
                  <CardTitle>Update</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button type="submit" className="w-full" disabled={isSubmitting}>
                    {isSubmitting ? "Updating..." : "Update Package"}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    className="w-full"
                    onClick={() => navigate("/manage-packages")}
                    disabled={isSubmitting}
                  >
                    Cancel
                  </Button>

                  <div className="text-muted-foreground space-y-2 pt-4 text-sm">
                    <p>• All fields marked with * are required</p>
                    <p>• Changes will be saved immediately</p>
                    <p>• Existing bookings won't be affected</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </form>
      </section>
    </MainLayout>
  );
}
