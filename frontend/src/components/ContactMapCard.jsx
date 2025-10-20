
const ContactMapCard = ({ title, location, icons, number, email }) => {
    return (
        <div className="grid gap-4 text-gray p-6 border-b-2 border-pink-300 max-w-[270px] shadow-2xl hover:shadow-4xl transition duration-300 ease-in-out mb-6 mx-5">
            <h2 className="text-lg tracking-wider font-semibold border-l-2 pl-2 border-pink-600">{title}</h2>
            <div className="flex w-full items-center gap-4">
                {icons.locationIcon}

                <p>{location}</p>

            </div>
            <div className="flex w-full items-center gap-4">
                {icons.phoneIcon}

                <p>{number}</p>
            </div>
            <div className="flex w-full items-center gap-4">
                {icons.emailIcon}
                {<p>{email}</p>}
            </div>
        </div>
    )
}

export default ContactMapCard