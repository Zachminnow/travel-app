import gridImage1 from "../assets/images/s1.jpeg";
import gridImage2 from "../assets/images/s2.jpeg";

const AboutGridBox = () => {
  return (
    <div className="relative w-full h-full flex flex-wrap ">
      <div
        className="w-[80%] h-[80%] absolute top-10 right-0 p-4 border-pink-600 border-2 rounded-sm"
        style={{
          backgroundImage: `url(${gridImage1})`,
          backgroundPosition: "center",
          backgroundSize: "cover",
        }}
      ></div>
      <div
        className="w-[44%] h-[44%] absolute bottom-10 left-0 p-4 border-pink-600 border-2 rounded-sm"
        style={{
          backgroundImage: `url(${gridImage2})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      ></div>
    </div>
  );
};

export default AboutGridBox;
