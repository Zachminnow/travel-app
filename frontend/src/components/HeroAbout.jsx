import bgImage from "../assets/images/A1.jpeg";
import { motion } from "framer-motion";
import { FaAirbnb } from "react-icons/fa";
import { MdOutlineTour } from "react-icons/md";
import { GiAirplaneDeparture } from "react-icons/gi";
import { RiHotelLine } from "react-icons/ri";
import AboutCard from "./AboutCard";

const HeroAbout = () => {
  const AboutData = [
    {
      title: "Our Mission",
      description: "To provide the best travel experiences.",
      icon: <FaAirbnb className="text-4xl text-white" />,
    },
    {
      title: "Our Vision",
      description: "To be the leading travel agency.",
      icon: <MdOutlineTour className="text-4xl text-white" />,
    },
    {
      title: "Our Values",
      description: "Customer satisfaction, integrity, and innovation.",
      icon: <GiAirplaneDeparture className="text-4xl text-white" />,
    },
    {
      title: "Our Services",
      description: "We offer a wide range of travel services.",
      icon: <RiHotelLine className="text-4xl text-white" />,
    },
  ];
  return (
    <motion.div
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      style={{
        backgroundImage: `linear-gradient(to right, rgba(0,0,0,0.6), rgba(0,0,0,0.2)), url(${bgImage})`,
        backgroundPosition: "center",
        backgroundSize: "cover",
      }}
      className="w-[1300px] h-[500px] flex flex-col rounded-lg justify-center items-center text-white"
    >
      <h1 className="text-4xl font-bold text-center mt-10">About Us</h1>
      <p className="text-lg text-center mt-4">
        We are a travel agency dedicated to providing the best travel
        experiences for our clients.
      </p>
      {
        AboutData.map((item,index)=>(
            <AboutCard key={index} title={item.title} description={item.description} icon={item.icon} />

        ))
      }
    </motion.div>
  );
};

export default HeroAbout;
