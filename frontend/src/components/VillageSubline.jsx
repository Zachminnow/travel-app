import img1 from "../assets/images/f1.jpeg";
import { FaCheckCircle } from "react-icons/fa";
const VillageSubline = () => {
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
    <div className="grid grid-cols-2 gap-2 items-center w-full ">
      <div className="w-full  h-full flex flex-col items-center justify-center text-start">
        <h1 className="text-start flex my-5 w-full px-5 font-allan text-2xl text-pink-600 font-bold">
          Bookmarksgrove, the headline of Alphabet Village subline.
        </h1>
        <p className="px-5 text-gray-800">
          Far far away, behind the word mountains, far from the countries
          Vokalia and Consonantia, there live the blind texts. Separated they
          live in Bookmarksgrove right at the coast of the Semantics.
        </p>
        <div className="grid grid-cols-2 gap-2 mt-5 w-full px-5">
          {Boxes.map((box, index) => (
            <div
              key={index}
              className="flex items-center my-2 hover:shadow-pink-300 p-2 rounded-lg border-2 border-transparent hover:shadow-md transition-all duration-300 cursor-pointer shadow-sm bg-slate-100"
            >
              {box.icon}
              <p className="ml-2 font-mono text-gray-800">{box.content}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="box">
        <img
          src={img1}
          alt="village-pic"
          className="w-full h-auto max-h-[420px] shadow-lg object-cover"
        />
      </div>
    </div>
  );
};

export default VillageSubline;
