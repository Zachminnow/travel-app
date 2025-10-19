
const ContactMapCard = ({ title, location, icon, number, email }) => {
    return (
        <div className="box">
            <h2>{title}</h2>
            <div className="box">
                {icon}
                <p>{location}</p>

            </div>
            <div className="box">
                {icon}
                <p>{number}</p>
            </div>
            <div className="box">
                {icon}
                {<p>{email}</p>}
            </div>
        </div>
    )
}

export default ContactMapCard