import React from "react";
import img1 from "../assets/images/e1.jpeg";
import { FaArrowUp } from "react-icons/fa";
import { FaCheckCircle } from "react-icons/fa";

const Bookmarksgrove = () => {
  const Boxes = [
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "Far far away, behind the word mountains.",
    },
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "Separated they live in Bookmarksgrove.",
    },
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "Far from the countries Vokalia and Consonantia.",
    },
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "Right at the coast of the Semantics.",
    },
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "A small river named Duden flows by their place.",
    },
    {
      icon: <FaCheckCircle className="text-lg text-pink-600" />,
      content: "Bookmarksgrove, where the texts live.",
    },
  ];

  return (
    <div className="grid md:grid-cols-2 grid-cols-1 gap-6 w-[95%] mx-auto h-full items-center justify-center py-8">
      <div className="flex items-center justify-center">
        <img
          src={img1}
          alt="Bookmarksgrove"
          className="w-full max-w-[700px] max-h-[500px] shadow-lg object-cover"
        />
      </div>

      <div className="flex flex-col items-center justify-center p-5">
        <h2 className="text-2xl md:text-3xl font-bold mb-4 font-allan text-pink-600 text-center md:text-left">
          Bookmarksgrove, the headline of Alphabet Village subline.
        </h2>
        <p className="text-gray-800 leading-relaxed text-center md:text-left">
          Far far away, behind the word mountains, far from the countries
          Vokalia and Consonantia, there live the blind texts. Separated they
          live in Bookmarksgrove right at the coast of the Semantics.
        </p>

        <div className="grid grid-cols-2 gap-4 mt-6 w-full">
          {Boxes.map((box, index) => (
            <div
              key={index}
              className="bg-slate-100 border-2 border-transparent hover:shadow-pink-300 p-2 rounded-lg flex  items-center text-center shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer"
            >
              {box.icon}
              <p className=" ml-3 font-mono text-sm mt-2 text-gray-700">
                {box.content}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Bookmarksgrove;
