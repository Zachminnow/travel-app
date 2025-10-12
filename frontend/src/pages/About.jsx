import React from "react";
import HeroAbout from "../components/HeroAbout";
import AboutUs from './../components/AboutUs';
import Bookmarksgrove from "../components/Bookmarksgrove";


const About = () => {
  return (
    <div className="  bg-white flex items-center justify-around flex-col  pt-0 pb-10 mt-0">
      <section className="w-[1280px] flex items-center justify-center  mt-0 pt-0">
        <HeroAbout />
      </section>
      <section className=" w-[1280px] mt-14 h-screen flex items-center justify-center">
        <AboutUs />
      </section>
       <section className=" w-[1280px] bg-white mt-14 min-h-screen flex items-center justify-center">
       <Bookmarksgrove /> 
      </section>
    </div>
  );
};

export default About;
