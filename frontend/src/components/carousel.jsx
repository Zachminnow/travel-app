import { OfferCard } from "./OfferCard";


export const Carousel = () => {
    const offers = [
        { image: "", title: "Special Offer 1", description: "Get 20% off on your next trip!", price: "$199" },
        { image: "", title: "Special Offer 2", description: "Get 30% off on your next trip!", price: "$299" },
        { image: "", title: "Special Offer 3", description: "Get 40% off on your next trip!", price: "$399" },
    ];
    return (
        <div>
            {offers.map((offer, index) => (
                <OfferCard key={index} offer={offer} />
            ))}
        </div>
    );
}