import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { TourCard } from "./TourCard";
import { useEffect, useState } from "react";
import { getTours } from "../services/apiServices";

export const TourCarousel = () => {
  const [tours, setTours] = useState([]);

  useEffect(() => {
    const fetchTours = async () => {
      try {
        const data = await getTours();
        setTours(data.results || []); 
      } catch (error) {
        console.error("Error fetching tours:", error);
        setTours([])
      }
    };
    fetchTours();
  }, []);

  const [emblaRef] = useEmblaCarousel({ loop: true }, [Autoplay()]);

  return (
    <div className="embla w-full overflow-hidden" ref={emblaRef}>
      <div className="flex">
        {tours.map((tour, index) => (
          <div
            key={index}
            className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3"
          >
            <TourCard tour={tour} />
          </div>
        ))}
      </div>
    </div>
  );
};
