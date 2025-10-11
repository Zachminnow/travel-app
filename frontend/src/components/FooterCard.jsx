import { Link } from "react-router-dom";
import { InputBox } from "./InputBox";
import { FaInstagram } from "react-icons/fa";
import { FaFacebookSquare } from "react-icons/fa";
import { FaLinkedin } from "react-icons/fa";

export const FooterCard = () => {
    const sendEmail = (e) => {
        e.preventDefault();
        alert("Thank you for subscribing!");
    }
  return (
    <div className="">
      <div className="grid grid-cols-3 gap-5 w-full">
        <div className="">
          <h2 className="font-allan text-2xl text-pink-600">Travola</h2>
          <p className="my-6">
            Your trusted travel partner for unforgettable journeys and
            experiences. In addition to our travel services, we also offer
            travel insurance to ensure your peace of mind while exploring the
            world with us.
          </p>
          <input
            type="email"
            placeholder="Enter your email"
            className="p-2 rounded-l-md w-[250px] focus:outline-none border-[0] text-black"
          />
          <button onClick={sendEmail} className="bg-pink-600 text-white p-2 rounded-r-md mt-2 hover:bg-pink-700">
            Subscribe
          </button>
        </div>
        <div className="flex flex-col justify-between items-center">
          <h1 className="border-b-2 border-white pb-10 w-full text-center">
            Navigation
          </h1>
          <Link className="hover:text-pink-600" to="/">Home</Link>
          <Link className="hover:text-pink-600" to="/about">About</Link>
          <Link className="hover:text-pink-600" to="/services">Services</Link>
        </div>
        <div className="flex flex-col justify-between items-center">
          <h1 className="border-b-2 border-white pb-10 w-full text-center">
            Need help?
          </h1>
          <div className="ml-4 border-l-[0.5px] border-pink-600 pl-2 box my-3 w-full">
            <p>Call us</p>
            <p>+1 234 567 890</p>
          </div>
          <div className="ml-4  border-l-[0.5px] border-pink-600 pl-2 box my-3 w-full">
            <p>Email us</p>
            <p>info@travola.com</p>
          </div>
          <div className="ml-4  border-l-[0.5px] border-pink-600 pl-2 box my-3 w-full">
            <p>Location</p>
            <p>123 Travel St, Wanderlust City</p>
          </div>
          <div className="ml-4  border-l-[0.5px] border-pink-600 pl-2 box my-3 w-full">
            <p>Follow us</p>
            <p>
              <FaInstagram
                className="inline mr-2 cursor-pointer hover:text-pink-600"
                size={24}
              />
              <FaFacebookSquare
                className="inline mr-2 cursor-pointer hover:text-pink-600"
                size={24}
              />
              <FaLinkedin
                className="inline mr-2 cursor-pointer hover:text-pink-600"
                size={24}
              />
            </p>
          </div>
        </div>
      </div>
      <div className="w-full text-center mt-8 border-t-2 border-white-600 pt-4">
        <p>
          &copy; {new Date().getFullYear()} Travola Agency. All rights reserved.
        </p>
        <p className="mt-2">
          Follow us on social media for the latest updates and offers!
        </p>
      </div>
    </div>
  );
};
