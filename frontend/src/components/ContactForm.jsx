import { FaPhone, FaAddressBook, FaMailBulk, FaUser } from "react-icons/fa"
import ContactInput from "./ContactInput"

const ContactForm = () => {
    const inputDetails = [{
        text: `Full name..`,
        icon: <FaUser size={20} className="text-pink-600" />,
        type: `text`
    }, {
        text: `Email address..`,
        icon: <FaMailBulk size={20} className="text-pink-600" />,
        type: `email`
    }, {
        text: `Phone number..`,
        icon: <FaPhone size={20} className="text-pink-600" />,
        type: `number`
    }, {
        text: `Address..`,
        icon: <FaAddressBook size={20} className="text-pink-600" />,
        type: `adress`
    }]
    return (
        <div className="flex flex-col w-full ">
            <div className="grid grid-cols-2 grid-rows-2 place-items-center">
                {
                    inputDetails.map((item, index) => (
                        <ContactInput key={index} text={item.text} icon={item.icon} type={item.type} />
                    ))
                }
            </div>
            <div className="py-2 my-4 flex items-center border-b-2 border-gray-300  justify-center">
                <textarea placeholder="Your Message.." className="focus:outline-none border-[1px]  rounded w-[60%] h-[150px] p-2" />
            </div>
            <div className="flex items-center justify-center w-full">
                <button className="bg-pink-600 text-white px-6 py-2 rounded hover:bg-pink-700 transition duration-300 ease-in-out h-[50px]">Send Message</button>
            </div>

        </div>
    )
}

export default ContactForm