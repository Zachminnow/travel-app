import React from "react";
import { RightBox } from "./RightBox";
import AboutGridBox from "./AboutGridBox";

const AboutUs = () => {
  return (
    <div className="grid grid-cols-2 gap-10 text-white px-5 h-full items-center">
      <div className="h-full flex flex-col justify-center gap-5">
        <h2 className="font-bold border-l-2 pl-2 border-pink-600 text-gray-800">About Us</h2>
        <h1 className="font-allan font-bold text-3xl text-pink-600">
          Plan Your Trip with Us
        </h1>
        <p className=" text-gray-800">
          Far far away, behind the word mountains, far from the countries
          Vokalia and Consonantia, there live the blind texts. Separated they
          live in Bookmarksgrove right at the coast of the Semantics, a large
          language ocean. A small river named Duden flows by their place and
          supplies it with the necessary regelialia. It is a paradisematic
          country she had a last view back on the skyline The Big Oxmox advised
          her not to do so, because there were thousands of bad Commas, wild
          Question Marks and devious Semikoli, but the Little Blind Text didn’t
          listen. She packed her seven versalia she had a last view back on the
          skyline of her hometown
        </p>
      </div>
      <div className=" h-full">
        <AboutGridBox />
      </div>
    </div>
  );
};

export default AboutUs;
