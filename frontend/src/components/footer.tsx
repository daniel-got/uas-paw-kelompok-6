import { Logo, LogoImage, LogoText } from "@/components/logo";
import { Link } from "react-router-dom";

interface MenuItem {
  title: string;
  links: {
    text: string;
    url: string;
  }[];
}

interface FooterProps {
  logo?: {
    url: string;
    src: string;
    alt: string;
    title: string;
  };
  tagline?: string;
  menuItems?: MenuItem[];
  copyright?: string;
  bottomLinks?: {
    text: string;
    url: string;
  }[];
}

const Footer = ({
  logo = {
    src: "/tree-palm.svg",
    alt: "Wanderlust Inn",
    title: "Wanderlust Inn",
    url: "/",
  },
  tagline = "Your journey begins here. Discover the world with us.",
  menuItems = [
    {
      title: "Explore",
      links: [
        { text: "Destinations", url: "/destinations" },
        { text: "Packages", url: "/packages" },
      ],
    },
    {
      title: "Services",
      links: [
        { text: "Book a Package", url: "/packages" },
        { text: "Become an Agent", url: "/sign-up" },
        { text: "My Bookings", url: "/dashboard" },
      ],
    },
    {
      title: "Company",
      links: [
        { text: "About Us", url: "/about" },
        { text: "Contact", url: "/contact" },
      ],
    },
    {
      title: "Support",
      links: [
        { text: "Help Center", url: "/help" },
      ],
    },
  ],
  copyright = "© 2025 Wanderlust Inn. All rights reserved.",
  bottomLinks = [],
}: FooterProps) => {
  return (
    <section className="py-32">
      <div className="container">
        <footer>
          <div className="grid grid-cols-2 gap-8 lg:grid-cols-6">
            <div className="col-span-2 mb-8 lg:mb-0">
              <div className="flex items-center gap-2 lg:justify-start">
                <Logo url="/">
                  <LogoImage
                    src={logo.src}
                    alt={logo.alt}
                    title={logo.title}
                    className="h-10 dark:invert"
                  />
                  <LogoText className="text-xl">{logo.title}</LogoText>
                </Logo>
              </div>
              <p className="mt-4 font-bold">{tagline}</p>
            </div>
            {menuItems.map((section, sectionIdx) => (
              <div key={sectionIdx}>
                <h3 className="mb-4 font-bold">{section.title}</h3>
                <ul className="text-muted-foreground space-y-4">
                  {section.links.map((link, linkIdx) => (
                    <li
                      key={linkIdx}
                      className="hover:text-primary font-medium"
                    >
                      {link.url.startsWith('http') || link.url.startsWith('mailto:') || link.url.startsWith('#') ? (
                        <a href={link.url}>{link.text}</a>
                      ) : (
                        <Link to={link.url}>{link.text}</Link>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="text-muted-foreground mt-24 flex flex-col justify-center gap-4 border-t pt-8 text-sm font-medium md:flex-row md:items-center">
            <p>{copyright}</p>
            {bottomLinks.length > 0 && (
              <ul className="flex gap-4">
                {bottomLinks.map((link, linkIdx) => (
                  <li key={linkIdx} className="hover:text-primary underline">
                    <a href={link.url}>{link.text}</a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </footer>
      </div>
    </section>
  );
};

export { Footer };
