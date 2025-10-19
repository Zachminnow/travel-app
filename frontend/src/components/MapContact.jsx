

const MapContact = () => {
    return (
        <div className="w-full h-[400px]">
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.8536172606995!2d36.82194621533186!3d-1.292065299050322!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x182f10d7d26e7e01%3A0x2a0e05f55eb3e1b2!2sNairobi%2C%20Kenya!5e0!3m2!1sen!2ske!4v1675844384302!5m2!1sen!2ske"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen=""
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
            ></iframe>
        </div>
    )
}

export default MapContact