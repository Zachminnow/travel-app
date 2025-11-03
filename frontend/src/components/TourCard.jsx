import { Button } from "./Button";

import { FaUser } from "react-icons/fa";
import { FaRegClock } from "react-icons/fa";
import { FaLuggageCart } from "react-icons/fa";

export const TourCard = ({ tour }) => {
  return (
    <div className="w-64 h-140 hover:scale-105 transition-transform duration-300 bg-white-500 rounded-lg shadow-md   flex flex-col relative">
      <div className="absolute left-[-11px] bottom-[45%] p-3 w-full z-100 my-1">
        <Button text={tour.title} link="/tours" />
      </div>
      <div style={{
        backgroundImage: `url(${tour.image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '170px',
      }}>
        
      </div>
      <div className="w-full z-1">
        {
          <p className="text-sm text-gray-600 mt-6 text-start px-2">
            {tour.description}
          </p>
        }
      </div>
      <div className=" p-3 flex  gap-2 flex-grow  content-center justify-evenly">
        <div className="flex flex-col justify-between items-center mb-2">
          <div className="flex justify-between items-center ">
            <FaRegClock className="inline-block mr-2 text-pink-600" />
            <p className="mr-2">Duration:</p>
          </div>

          <p>{tour.duration}</p>
        </div>
        <div className="flex justify-between items-center flex-col  h-10">

            <div className="flex  justify-between items-center ">
               <FaLuggageCart className="inline-block mr-2 text-pink-600" />
               <p className="mr-2">Space:</p>
            </div>
          <p>{tour.space}</p>
        </div>
      </div>
      <div className="flex justify-between items-center p-3 border-t border-gray-200">
        <p className="font-bold text-gray-800">{tour.price}</p>
        <p className="bg-pink-600 cursor-pointer text-white w-[100px] text-center h-[40px] items-center content-center justify-center rounded-lg hover:bg-pink-700  flex">
          Book Now!
        </p>
      </div>
    </div>
  );
};
