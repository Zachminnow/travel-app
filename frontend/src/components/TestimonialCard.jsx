


export const TestimonialCard = ({ name, location, feedback, rating, platform }) => {
    return(
        <div className="inline-block p-4 m-4 w-[95%] h-[440px] bg-[#FEB9B9] rounded-lg shadow-md hover:scale-105 transition-transform duration-300 cursor-pointer relative">
            <div className="bg-pink-600 w-[100px] h-10 rounded-sm items-center content-center justify-center flex absolute top-10 right-0 ">
            <img src={rating} alt="Stars" className="w-20" />

            </div>
            <div className="flex w-full flex-wrap py-10 my-14">
                <p className=" flex flex-wrap text-wrap text-2xl text-gray-800">{feedback}</p>
            </div>
            <div className="flex items-center gap-3 content-center justify-between w-[200px]">
                {platform}
                <h3 className="font-bold">{name}</h3>
                <p className="text-sm text-gray-600">{location}</p>
            </div>
        </div>
    )
}