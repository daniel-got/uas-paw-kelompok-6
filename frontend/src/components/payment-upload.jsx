import PropTypes from "prop-types";
import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Upload, X, CheckCircle, AlertCircle, Clock, QrCode, Image } from "lucide-react";
import { toast } from "sonner";
import { API_BASE_URL } from "@/services/api";

export function PaymentUpload({
  totalPrice,
  paymentStatus = "unpaid",
  paymentProofUrl,
  paymentRejectionReason,
  onUpload,
}) {
  const [selectedFile, setSelectedFile] = useState(null);

  // Convert relative URL to full URL
  const getFullProofUrl = (url) => {
    if (!url) return null;
    if (url.startsWith("http")) return url;
    return `${API_BASE_URL}${url}`;
  };

  const [previewUrl, setPreviewUrl] = useState(getFullProofUrl(paymentProofUrl));
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      toast.error("Please upload an image file");
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error("File size must be less than 5MB");
      return;
    }

    setSelectedFile(file);

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setPreviewUrl(getFullProofUrl(paymentProofUrl));
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    try {
      await onUpload(selectedFile);
      toast.success("Payment proof uploaded successfully!");
    } catch {
      toast.error("Failed to upload payment proof");
    } finally {
      setIsUploading(false);
    }
  };

  const getStatusBadge = () => {
    switch (paymentStatus) {
      case "verified":
        return (
          <Badge className="bg-green-500 hover:bg-green-600">
            <CheckCircle className="mr-1 h-3 w-3" />
            Payment Verified
          </Badge>
        );
      case "pending_verification":
        return (
          <Badge className="bg-yellow-500 hover:bg-yellow-600">
            <Clock className="mr-1 h-3 w-3" />
            Pending Verification
          </Badge>
        );
      case "rejected":
        return (
          <Badge variant="destructive">
            <AlertCircle className="mr-1 h-3 w-3" />
            Payment Rejected
          </Badge>
        );
      default:
        return (
          <Badge variant="secondary">
            <AlertCircle className="mr-1 h-3 w-3" />
            Payment Required
          </Badge>
        );
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Payment Information</CardTitle>
            <CardDescription>Complete your payment via QRIS</CardDescription>
          </div>
          {getStatusBadge()}
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Payment Amount */}
        <div className="bg-muted rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground text-sm font-medium">Total Amount</span>
            <span className="text-2xl font-bold">${totalPrice.toFixed(2)}</span>
          </div>
        </div>

        {/* QRIS Code */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <QrCode className="h-5 w-5" />
            <Label>Scan QRIS Code</Label>
          </div>
          <div className="flex justify-center rounded-lg border-2 border-dashed p-6">
            <div className="space-y-2 text-center">
              <div className="bg-muted mx-auto flex h-48 w-48 items-center justify-center rounded-lg">
                <QrCode className="text-muted-foreground h-24 w-24" />
              </div>
              <p className="text-muted-foreground text-sm">
                Scan this QR code with your mobile banking app
              </p>
              <p className="text-muted-foreground text-xs">
                Demo QRIS - In production, this would be a real QR code
              </p>
            </div>
          </div>
        </div>

        {/* Rejection Reason */}
        {paymentStatus === "rejected" && paymentRejectionReason && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              <strong>Payment Rejected:</strong> {paymentRejectionReason}
              <br />
              <span className="text-xs">Please upload a valid payment proof.</span>
            </AlertDescription>
          </Alert>
        )}

        {/* Upload Section */}
        {paymentStatus !== "verified" && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Image className="h-5 w-5" />
              <Label>Upload Payment Proof</Label>
            </div>

            {/* Preview */}
            {previewUrl && (
              <div className="relative">
                <img
                  src={previewUrl}
                  alt="Payment proof preview"
                  className="h-48 w-full rounded-lg border object-cover"
                  onError={(e) => {
                    const target = e.target;
                    target.src =
                      'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200"><rect fill="%23f0f0f0" width="400" height="200"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%23999">Failed to load image</text></svg>';
                    console.error("Failed to load payment proof preview");
                  }}
                />
                {selectedFile && (
                  <Button
                    type="button"
                    variant="destructive"
                    size="icon"
                    className="absolute top-2 right-2"
                    onClick={handleRemove}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>
            )}

            {/* File Input */}
            <div className="flex gap-2">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                className="flex-1"
                disabled={paymentStatus === "pending_verification"}
              >
                <Upload className="mr-2 h-4 w-4" />
                {previewUrl ? "Change Image" : "Select Image"}
              </Button>
              {selectedFile && (
                <Button
                  type="button"
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="flex-1"
                >
                  {isUploading ? "Uploading..." : "Upload Proof"}
                </Button>
              )}
            </div>

            <p className="text-muted-foreground text-xs">Accepted formats, PNG, JPEG (Max 5MB)</p>
          </div>
        )}

        {/* Status Messages */}
        {paymentStatus === "pending_verification" && (
          <Alert>
            <Clock className="h-4 w-4" />
            <AlertDescription>
              Your payment proof is under review. The agent will verify it soon.
            </AlertDescription>
          </Alert>
        )}

        {paymentStatus === "verified" && (
          <Alert className="border-green-500 bg-green-50 dark:bg-green-950">
            <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
            <AlertDescription className="text-green-600 dark:text-green-400">
              Payment verified Your booking is confirmed.
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}

PaymentUpload.propTypes = {
  totalPrice: PropTypes.number.isRequired,
  paymentStatus: PropTypes.oneOf(["unpaid", "pending_verification", "verified", "rejected"]),
  paymentProofUrl: PropTypes.string,
  paymentRejectionReason: PropTypes.string,
  onUpload: PropTypes.func.isRequired,
};
