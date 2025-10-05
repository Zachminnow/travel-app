import { OfferCard } from "./OfferCard";
import image1 from "../assets/images/c1.jpeg";
import image2 from "../assets/images/c2.jpeg";
import image3 from "../assets/images/c3.jpeg";
import image4 from "../assets/images/c4.jpeg";
import image5 from "../assets/images/c5.jpeg";


export const Carousel = () => {
    const offers = [
        { image: image1, title: "Special Offer 1", description: "Get 20% off on your next trip!", price: "$199" },
        { image: image2, title: "Special Offer 2", description: "Get 30% off on your next trip!", price: "$299" },
        { image: image3, title: "Special Offer 3", description: "Get 40% off on your next trip!", price: "$399" },
        { image: image4, title: "Special Offer 4", description: "Get 50% off on your next trip!", price: "$499" },
        { image: image5, title: "Special Offer 5", description: "Get 60% off on your next trip!", price: "$599" },
    ];
    return (
        <div>
            {offers.map((offer, index) => (
                <OfferCard key={index} offer={offer} />
            ))}
        </div>
    );
}