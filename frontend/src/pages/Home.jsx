import React from "react";
import sliderImage1 from "../assets/images/slider-image-1.jpeg";
import sliderImage2 from "../assets/images/slider-image-2.jpeg";
import sliderImage3 from "../assets/images/slider-image-3.jpeg";

const Home = () => {
  const sliderImages = [sliderImage1, sliderImage2, sliderImage3];

  return (
    <div className=" bg-[#EFE9EB] flex items-center justify-center">
      <div className="min-w-full flex justify-center items-center">
        <div
          className="w-[1380px] h-[600px] relative flex items-center justify-center bg-cover bg-center rounded-lg shadow-lg flex-col"
          style={{
            backgroundImage: `linear-gradient(to right, rgba(0,0,0,0.6), rgba(0,0,0,0.2)), url(${sliderImages[0]})`,
          }}
        >
          <h1 className="text-white text-4xl font-bold z-10">
            Explore the <span className="bg-pink-400">World</span> with Us
          </h1>
          <p className="text-white mt-4 z-10 max-w-xl text-center">
            Discover breathtaking destinations and unforgettable experiences.A journey of a thousand miles begins with a single step.
            Experience the beauty of the world like never before.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
