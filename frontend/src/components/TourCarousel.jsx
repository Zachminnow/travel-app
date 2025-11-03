import { useState, useEffect } from "react";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { TourCard } from "./TourCard";
import api from "../api/axios";

export const TourCarousel = () => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 5000 }),
  ]);

  const [TourOffers, setTourOffers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch tours from API
  useEffect(() => {
    const fetchTours = async () => {
      try {
        setLoading(true);
        const response = await api.get("tours/", {
          params: {
            page_size: 10,
            ordering: "-created_at",
          },
        });

        // Transform API data to match existing TourCard structure
        const toursData = response.data.results.map((tour) => ({
          image: tour.image_url || "/placeholder.jpg",
          title: tour.title,
          description: tour.description?.substring(0, 80) + "..." || 
                      "Explore this amazing destination",
          price: tour.price && tour.currency 
                ? `${tour.currency} ${tour.price}` 
                : "Contact for price",
          id: tour.id,
          duration: `${tour.duration_dates} Days`,
          space: tour.max_participants,
          slug: tour.slug,
          destination: tour.destination_name,
        }));

        setTourOffers(toursData);
      } catch (error) {
        console.error("Error fetching tours:", error);
        setTourOffers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTours();
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
              <div className="bg-gray-200 animate-pulse rounded-lg h-96"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="embla w-full overflow-hidden" ref={emblaRef}>
      <div className="flex">
        {TourOffers.map((TourOffers, index) => (
          <div
            key={index}
            className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3"
          >
            <TourCard TourOffers={TourOffers} />
          </div>
        ))}
      </div>
    </div>
  );
};