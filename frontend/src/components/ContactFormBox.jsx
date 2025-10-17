import ContactForm from "./ContactForm"
import ContactInfoBox from "./ContactInfoBox"

const ContactFormBox = () => {
  return (
    <div className="grid lg:grid-cols-2 gap-4 w-full bg-white py-4">
        <ContactForm/>
        <ContactInfoBox/>
    </div>
  )
}

export default ContactFormBox