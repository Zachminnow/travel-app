export const OfferCard = ({ offer }) => {
  return (
    <div className="offer-card">
      <img src={offer.image} alt={offer.title} />
      <h3>{offer.title}</h3>
      <p>{offer.description}</p>
      <span>{offer.price}</span>
    </div>
  );
};
