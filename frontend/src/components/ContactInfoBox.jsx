import image1 from '../assets/images/q1.jpeg'
import { FaMailBulk, FaPhone } from "react-icons/fa"
const ContactInfoBox = () => {
    return (
        <div className=" p-4 rounded-lg flex flex-col gap-4 justify-center items-center">
            <div className="flex flex-col items-center justify-center  shadow-xl min-w-[300px]  rounded-lg min-h-[220px] text-start hover:shadow-2xl transition duration-300 ease-in-out p-4 gap-4">
                <div className="w-full px-4">
                    <h1 className="border-l-pink-600 font-allan font-bold font-2xl border-l-2 pl-2 mb-5 text-start flex  w-full tracking-wider">Why Book With Us?</h1>
                    <ol className=" w-full text-start ">
                        <li>Best Price Guarantee</li>
                        <li>24/7 Customer Support</li>
                        <li>Wide Range of Destinations</li>
                        <li>Easy Booking Process</li>
                        <li>Trusted by Thousands</li>
                    </ol>
                </div>

            </div>
            <div
            style={{
                backgroundImage: `linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),url(${image1})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
            className="flex flex-col items-center justify-center  w-[300px] bg-gray-600 rounded-lg min-h-[220px] p-4 gap-4 text-start shadow-xl hover:shadow-2xl transition duration-300 ease-in-out">
                <h1 className="border-l-pink-600 font-allan font-bold font-2xl border-l-2 pl-2 mb-5 text-start flex  w-full text-white tracking-wider">
                    Got a Question?
                </h1>
                <p className="text-white text-start">
                    Do not hesitate to give us a call. We are an expert team and we are happy to talk to you.
                </p>
                <div className="flex w-full px-4 justify-start gap-5">
                    <FaPhone size={30} className="text-pink-600" />

                    <strong className='text-white'>+1 234 567 890</strong>
                </div>
                <div className="flex w-full px-4 justify-start gap-5">
                    <FaMailBulk size={30} className="text-pink-600" />
                    <p className="text-white">
                        travolaagency@gmail.com
                    </p>
                </div>
            </div>

        </div>

    )
}

export default ContactInfoBox