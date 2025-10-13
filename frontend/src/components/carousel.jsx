import { useState, useEffect } from "react";
import { OfferCard } from "./OfferCard";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import api from "../api/axios";

export const Carousel = () => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 7000 }),
  ]);

  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch featured destinations from API
  useEffect(() => {
    const fetchOffers = async () => {
      try {
        setLoading(true);
        const response = await api.get("destinations/featured/");

        // Transform API data to match existing OfferCard structure
        const offersData = response.data.map((dest) => ({
          image: dest.image_url || "/placeholder.jpg",
          title: dest.name,
          description: `${dest.tour_count} Tours Available`,
          id: dest.id,
          slug: dest.slug,
          country: dest.country,
        }));

        setOffers(offersData);
      } catch (error) {
        console.error("Error fetching destinations:", error);
        setOffers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchOffers();
  }, []);

  // Loading skeleton
  if (loading) {
    return (
      <div className="embla w-full overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {[...Array(5)].map((_, index) => (
            <div
              key={index}
              className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3"
            >
              <div className="bg-gray-200 animate-pulse rounded-lg h-80"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="embla w-full overflow-hidden" ref={emblaRef}>
      <div className="flex">
        {offers.map((offer, index) => (
          <div
            key={index}
            className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3"
          >
            <OfferCard offer={offer} />
          </div>
        ))}
      </div>
    </div>
  );
};