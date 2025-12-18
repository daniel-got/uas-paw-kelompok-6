import PropTypes from "prop-types";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AspectRatio } from "@/components/ui/aspect-ratio";

export const NewsletterSection = ({
  title = "Stay Connected with Wonderfull Inn",
  description = "Never miss a moment with Renee Connected, your go-to platform for updates, articles and exclusive content.",
  imageUrl = "https://images.unsplash.com/photo-1540541338287-41700207dee6?q=80&w=2000&auto=format&fit=crop",
}) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle newsletter subscription
    // TODO: Integrate with newsletter API
    setEmail("");
    navigate("/contact");
  };

  return (
    <section className="border-border overflow-hidden rounded-lg border">
      <div className="grid gap-0 md:grid-cols-2">
        {/* Image Side */}
        <div className="order-2 md:order-1">
          <AspectRatio ratio={16 / 10}>
            <img src={imageUrl} alt="Stay connected" className="h-full w-full object-cover" />
          </AspectRatio>
        </div>

        {/* Content Side */}
        <div className="bg-card order-1 flex flex-col justify-center p-8 md:order-2 md:p-12">
          <div className="space-y-6">
            <div className="space-y-4">
              <h2 className="text-foreground text-2xl leading-tight font-bold md:text-3xl">
                {title}
              </h2>
              <p className="text-muted-foreground text-sm leading-relaxed md:text-base">
                {description}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
             

              <Button
                type="submit"
                className="bg-primary text-primary-foreground hover:bg-primary/90 w-full"
              >
                Contact Us
              </Button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

NewsletterSection.propTypes = {
  title: PropTypes.string,
  description: PropTypes.string,
  imageUrl: PropTypes.string,
};
