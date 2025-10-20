import React from 'react'
import { FaMapMarkerAlt, FaPhone, FaMailBulk } from "react-icons/fa"
import MapContact from './MapContact'
import ContactMapCard from './ContactMapCard'
const ContactMapBox = () => {
    const contactInfo =[{
        title: "Africa Location",
        location: "123 Travel St, Wanderlust City, Country",
        number: "+1 234 567 890",
        email: "info@travelagency.com"
    },{
        title: "America Location",
        location: "456 Travel Ave, Adventure City, Country",
        number: "+1 987 654 321",
        email: "info@travelagency.com"
    }]
    const icons =[{
        locationIcon: <FaMapMarkerAlt size={20} className='text-pink-600' />,
        phoneIcon: <FaPhone size={20} className='text-pink-600' />,
        emailIcon: <FaMailBulk size={20} className='text-pink-600' />
    }]
  return (
    <div className="grid w-full  lg:grid-cols-2 md:grid-cols-1 place-content-center">
        <div className=" flex flex-col justify-center items-start py-10 lg:py-0">{
            contactInfo.map((info, index) => (
                <ContactMapCard
                    key={index}
                    title={info.title}
                    location={info.location}
                    number={info.number}
                    email={info.email}
                    icons={icons[0]}
                />
            ))}
        </div>
        <div className="sm:hidden lg:block p-5">
            <MapContact />
        </div>
    </div>
  )
}

export default ContactMapBox