import React from "react";
import sliderImage1 from "../assets/images/slider-image-1.jpeg";
import sliderImage2 from "../assets/images/slider-image-2.jpeg";
import sliderImage3 from "../assets/images/slider-image-3.jpeg";
import aboutImage from "../assets/images/About-img.png";
import { TravelInput } from "../components/Travel-Input";
import { Button } from "../components/Button";
import { RightBox } from "../components/RightBox";
import { GridBox } from "../components/GridBox";
import { Carousel } from "../components/carousel";

const Home = () => {
  const sliderImages = [sliderImage1, sliderImage2, sliderImage3];

  return (
    <div className=" bg-[#EFE9EB] flex items-center justify-center flex-col ">
      <section className="w-full  flex flex-col justify-center items-center gap-0">
        <div className="min-w-full flex justify-center items-center">
          <div
            className="w-[1300px] h-[600px] relative flex items-center justify-center bg-cover bg-center rounded-lg shadow-lg flex-col"
            style={{
              backgroundImage: `linear-gradient(to right, rgba(0,0,0,0.6), rgba(0,0,0,0.2)), url(${sliderImages[0]})`,
            }}
          >
            <h1 className="text-white text-4xl font-bold z-10">
              Explore the <span className="bg-pink-600 w-[120px]">World</span>{" "}
              with Us
            </h1>
            <p className="text-white mt-4 z-10 max-w-xl text-center">
              Discover breathtaking destinations and unforgettable experiences.A
              journey of a thousand miles begins with a single step. Experience
              the beauty of the world like never before.
            </p>
          </div>
        </div>
        <TravelInput />
      </section>
      <section>
        <div className="bg-[#EFE9EB]p-4 rounded-lg shadow-lg w-[1180px] flex  justify-between gap-5 items-center mt-10">
          <div className="w-[50%] flex justify-center items-center">
            <img src={aboutImage} alt="About Us" />
          </div>

          <div className="w-[50%]">
            <RightBox />
          </div>
        </div>
      </section>
      <section>
        <div className="bg-[#EFE9EB] p-4 rounded-lg shadow-lg w-[1180px]  justify-between gap-5 items-start mt-10 flex flex-col ">
          <div className=" flex flex-col w-full justify-center items-start  text-start mb-6">
            <h2 className="text-1xl font-bold text-[#2E2E2E]  mb-4 items-start border-l-2 pl-2 border-pink-600">
              Amaizing destinations
            </h2>
            <h1 className="text-2xl font-bold text-pink-600 font-allan mb-4">
              Explore the world's most beautiful places with our curated travel
            </h1>
          </div>
          <GridBox />
          <div className="box w-full flex justify-center items-center mt-6">
            <Button text="View All Destinations" link="/destinations" />
          </div>
        </div>
      </section>
      <section>
        <div className="bg-[#EFE9EB] p-4 rounded-lg shadow-lg w-[1180px]  justify-between gap-5 items-start mt-10 flex flex-col mb-10">
          <div className=" flex flex-col w-full justify-center items-start  text-start mb-6">
            <h2 className="text-1xl font-bold text-[#2E2E2E]  mb-4 items-start border-l-2 pl-2 border-pink-600">Amazing offers
            </h2>
            <h1 className="text-2xl font-bold text-pink-600 font-allan mb-4">
              Discover exclusive travel deals and offers for your next adventure.
            </h1>
          </div>
          <div className="box w-full flex justify-center items-center mt-6">
            <Carousel />
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
