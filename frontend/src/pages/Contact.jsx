
import ContactHero from '../components/ContactHero';
import ContactFormBox from '../components/ContactFormBox';
import ContactMapBox from '../components/ContactMapBox';
import { motion } from "framer-motion";
import { FooterCard } from '../components/FooterCard';


const Contact = () => {
  return (
    <div className="  m-0 p-0 items-center justify-center flex flex-col">
      <div className='flex flex-col bg-white items-center justify-center'>
        <ContactHero />
        <ContactFormBox />
        <ContactMapBox />
      </div>
      <motion.footer
        initial={{ opacity: 0, x: 80 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
        viewport={{ once: true, amount: 0.3 }}
        className="w-full bg-[#2E2E2E] text-white p-4 flex flex-col items-center justify-center mt-10"
      >
        <FooterCard />
      </motion.footer>

    </div>
  );
};

export default Contact;