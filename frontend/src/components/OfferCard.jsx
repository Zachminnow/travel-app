
export const OfferCard = ({ offer }) => {
  return (
    <div className="w-64 h-140 hover:scale-105 transition-transform duration-300 bg-white rounded-lg shadow-md overflow-hidden flex-shrink-0">
      <img
        src={offer.image}
        alt={offer.title}
        className="w-full h-[300px] object-cover"
      />
      <div className="p-3">
       
        <p className="text-sm text-white flex items-center content-center text-center absolute top-0 left-0 w-10 h-7 pl-2 bg-pink-600">
          {offer.description}
        </p>

        <div className="flex content-evenly items-center justify-between">
             <h3 className="font-bold text-lg">{offer.title}</h3>
             <h2 className="w-[70px] h-[40px] rounded-lg bg-pink-600 text-white text-center items-center content-center cursor-pointer hover:bg-pink-700">{offer.price}</h2>
         
        </div>
      </div>
    </div>
  );
};
