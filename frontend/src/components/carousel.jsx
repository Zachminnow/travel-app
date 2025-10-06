import { OfferCard } from "./OfferCard";
import image1 from "../assets/images/c1.jpeg";
import image2 from "../assets/images/c2.jpeg";
import image3 from "../assets/images/c3.jpeg";
import image4 from "../assets/images/c4.jpeg";
import image5 from "../assets/images/c5.jpeg";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";

export const Carousel = () => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 7000 }),
  ]);

  const offers = [
    {
      image: image1,
      title: "Kenya",
      description: "18% ",
      price: "$199",
      id: 1,
    },
    {
      image: image2,
      title: "India",
      description: "20% ",
      price: "$299",
      id: 2,
    },
    {
      image: image3,
      title: "Transylvania",
      description: "14% ",
      price: "$399",
      id: 3,
    },
    {
      image: image4,
      title: "Kilimanjaro",
      description: "15% ",
      price: "$499",
      id: 4,
    },
    {
      image: image5,
      title: "Uganda",
      description: "10% ",
      price: "$599",
      id: 5,
    },
  ];

  return (
    <div className="embla w-full overflow-hidden"  ref={emblaRef}>
      <div className="flex">
        {offers.map((offer, index) => (
          <div
            key={index}
            className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3"
          >
            <OfferCard
             
              offer={offer}
            />
          </div>
        ))}
      </div>
    </div>
  );
};
