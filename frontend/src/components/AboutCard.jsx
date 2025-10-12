import React from "react";

const AboutCard = ({ title, description, icon }) => {
  return (
    <div className="bg-white-300 p-4 rounded-lg shadow-md bg-white flex flex-col items-center text-center hover:border-pink-600 border-2 duration-300 cursor-pointer transition-colors">
      <h2 className="text-xl font-bold mb-2 text-pink-600">{title}</h2>
      <p className="text-gray-700">{description}</p>
      <div className="mt-4">{icon}</div>
    </div>
  );
};

export default AboutCard;
