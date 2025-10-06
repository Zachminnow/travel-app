import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { TourCard } from "./TourCard";
import image1 from "../assets/images/b1.jpeg";
import image2 from "../assets/images/b2.jpeg";
import image3 from "../assets/images/b3.jpeg";
import image4 from "../assets/images/b4.jpeg";
import image5 from "../assets/images/b5.jpeg";


export const TourCarousel = () => {

    const TourOffers = [
        {
            image: image1,
            title: "Tanzania",
            description: "Explore the stunning landscapes and wildlife of Tanzania.",
            price: "$799",
            id: 1,
            duration: "7 Days",
            space: 4,
        },
        {
            image: image2,
            title: "Dakota",
            description: "Explore the historic cities and beautiful countryside of Dakota.",
            price: "$799",
            id: 2,
            duration: "5 Days",
            space: 10,
        },
        {
            image: image3,
            title: "Egypt",
            description: "Explore the historic cities and beautiful pyramids of Egypt.",
            price: "$799",
            id: 3,
            duration: "6 Days",
            space: 14,
        },
        {
            image: image4,
            title: "London",
            description: "Explore the historic cities and beautiful architecture of London.",
            price: "$799",
            id: 4,
            duration: "5 Days",
            space: 20,
        },{
            image: image5,
            title: "Tokyo",
            description: "Explore the historic cities and beautiful culture of Tokyo.",
            price: "$799",
            id: 5,
            duration: "7 Days",
            space: 10,
        }
    ]
  const [emblaRef] = useEmblaCarousel({ loop: true });
  return <div className="embla w-full overflow-hidden" ref={emblaRef}>

    <div className="flex">
    {
        TourOffers.map((TourOffers, index) => (
            <div key={index} className="flex-[0_0_80%] sm:flex-[0_0_50%] md:flex-[0_0_33.33%] lg:flex-[0_0_25%] p-3">
                <TourCard TourOffers={TourOffers} />
            </div>
        ))
    }
    </div>
    
  </div>;
};
