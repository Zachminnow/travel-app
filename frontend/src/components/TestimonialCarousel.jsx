import { TestimonialCard } from "./TestimonialCard";
import useEmblaCarousel from "embla-carousel-react";
import image from "../assets/images/stars.png";
import { FaInstagram } from "react-icons/fa";
import { FaFacebookSquare } from "react-icons/fa";
import { FaLinkedin } from "react-icons/fa";
import Autoplay from "embla-carousel-autoplay";

export const TestimonialCarousel = () => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 7000 }),
  ]);
  

  const Testimonies = [
    {
      name: "John Doe",
      location: "New York, USA",
      feedback:
        "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean.",
      rating: image,
      id: 1,
      platform: <FaInstagram />,
    },
    {
      name: "Jane Smith",
      location: "London, UK",
      feedback:
        "A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.",
      rating: image,
      id: 2,
      platform: <FaFacebookSquare />,
    },
    {
      name: "Carlos Rodriguez",
      location: "Madrid, Spain",
      feedback:
        "Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life. One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar.",
      rating: image,
      id: 3,
      platform: <FaLinkedin />,
    },
  ];

  return (
    <div className="overflow-hidden embla" ref={emblaRef}>
      <div className="whitespace-nowrap">
        {Testimonies.map((testimony) => (
          <TestimonialCard key={testimony.id} {...testimony} />
        ))}
      </div>
    </div>
  );
};
