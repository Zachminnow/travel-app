import gridImage1 from "../assets/images/grid-pic-1.jpeg";
import gridImage2 from "../assets/images/slider-image-2.jpeg";
import gridImage3 from "../assets/images/grid-pic-7.jpeg";
import gridImage4 from "../assets/images/grid-pic-2.jpeg";
import { Button } from "./Button";

export const GridBox = () => {
  return (
    <div className="grid-container">
      <div
        className=" rounded-sm mr-1 transition-transform duration-300 hover:scale-105"
        style={{
          gridArea: "box-1",
          width: "540px",
          marginRight: "20px",
          backgroundImage: `url(${gridImage2})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Button text="Tokyo" link="/destinations/tokyo" />
      </div>
      <div
        className="rounded-sm ml-2 transition-transform duration-300 hover:scale-105"
        style={{
          gridArea: "box-2",
          width: "550px",
          backgroundImage: `url(${gridImage1})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Button  text="Africa" link="/destinations/africa" />
      </div>
      <div
        className=" rounded-sm transition-transform duration-300 hover:scale-105"
        style={{
          gridArea: "box-3",
          width: "300px",
          backgroundImage: `url(${gridImage3})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Button text="London" link="/destinations/tokyo" />
      </div>
      <div
        className="rounded-sm transition-transform duration-300 hover:scale-105"
        style={{
          gridArea: "box-4",
          width: "220px",
          backgroundImage: `url(${gridImage4})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Button text="Brazil" link="/destinations/brazil" />
      </div>
    </div>
  );
};
