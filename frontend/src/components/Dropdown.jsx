import React from 'react';
import { MdLocationOn, MdCalendarToday, MdSearch, MdPeople } from 'react-icons/md';
import { FaPlane, FaMapMarkerAlt } from 'react-icons/fa';
import { IoCalendarOutline, IoLocationOutline } from 'react-icons/io5';


export const Dropdown = ({ months, travelTypes, text }) => {

  return (
    <div className="flex bg-slate-50 rounded-lg border-[1px] border-pink-600 justify-center items-center h-[50px]">
        {
            months ? <IoCalendarOutline className="text-pink-600 mx-2" size={24} /> : <FaPlane className="text-pink-600 mx-2" size={24} />
        }
     
      <p className="p-3">{text}</p>
      <select className="p-2 border border-pink-600rounded-md mx-2 ">
        {months
          ? months.map((month, index) => (
              <option key={index} value={month}>
                {month}
              </option>
            ))
          : travelTypes.map((type, index) => (
              <option key={index} value={type}>
                {type}
              </option>
            ))}
      </select>
    </div>
  );
};
