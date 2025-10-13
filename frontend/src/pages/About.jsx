import React from "react";
import HeroAbout from "../components/HeroAbout";
import AboutUs from "./../components/AboutUs";
import Bookmarksgrove from "../components/Bookmarksgrove";
import HeadlineSubline from "../components/HeadlineSubline";
import VillageSubline from "../components/VillageSubline";
import { motion } from "framer-motion";
import { FooterCard } from "../components/FooterCard";

const About = () => {
  return (
    <div className="  bg-white flex items-center justify-around flex-col  pt-0  mt-0">
      <section className="w-[1280px] flex items-center justify-center  mt-0 pt-0">
        <HeroAbout />
      </section>
      <section className=" w-[1280px] mt-14 h-screen flex items-center justify-center">
        <AboutUs />
      </section>
      <section className=" w-[1280px] bg-white mt-14 min-h-screen flex flex-col items-center justify-center">
        <Bookmarksgrove />
        <HeadlineSubline />
      </section>
      <section className=" w-[1280px] bg-white mt-14 min-h-screen flex items-center justify-center">
        <VillageSubline />
      </section>
      <motion.footer
        initial={{ opacity: 0, x: 80 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
        viewport={{ once: true, amount: 0.3 }}
        className="w-full bg-[#2E2E2E] text-white p-4 flex flex-col items-center justify-center mt-10"
      >
        <FooterCard />
      </motion.footer>
    </div>
  );
};

export default About;
