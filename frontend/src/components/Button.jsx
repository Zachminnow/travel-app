import { Link } from "react-router-dom";

export const Button = ({ text, link }) => {
  return (
    <button className="bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700 transition-colors w-[200px] h-[50px]">
      <Link to={link}>{text}</Link>
    </button>
  );
};
