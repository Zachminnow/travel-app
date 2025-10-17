
import ContactHero from '../components/ContactHero';
import ContactFormBox from '../components/ContactFormBox';


const Contact = () => {
  return (
    <div className="  m-0 p-0 items-center justify-center flex flex-col">
      <div className='flex flex-col bg-white items-center justify-center'>
        <ContactHero />
        <ContactFormBox />
      </div>


    </div>
  );
};

export default Contact;