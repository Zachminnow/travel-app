import React from "react";
// Import icons from react-icons
import {
  MdLocationOn,
  MdCalendarToday,
  MdSearch,
  MdPeople,
} from "react-icons/md";
import { FaPlane, FaMapMarkerAlt } from "react-icons/fa";
import { IoCalendarOutline, IoLocationOutline } from "react-icons/io5";
import { Dropdown } from "./Dropdown";
import { Button } from "./Button";

export const TravelInput = () => {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const travelTypes = ["Adventure", "Relaxation", "Cultural", "Wildlife"];

  return (
    <div className="bg-[#2E2E2E] p-4 rounded-lg shadow-lg w-[1180px] h-[100px] mt-5 flex  justify-between gap-5 items-center">
      <div className="flex bg-slate-50 rounded-lg border-[1px] border-pink-600 justify-evenly items-center w-[300px] h-[50px]">
        <FaMapMarkerAlt className="text-pink-600 mx-2" size={24} />
        <input
          type="text"
          placeholder="Search for destinations..."
          className="p-2 focus:outline-none border-[0] rounded-md"
        />
      </div>

      <Dropdown months={months} text="When?" />
      <Dropdown travelTypes={travelTypes} text="Travel Type" />
      <Button text="Find Now" />
    </div>
  );
};
