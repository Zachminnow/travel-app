
import image1 from '../assets/images/d22.jpeg'
const DestinationHero = () => {
    return (
        <div
            style={{
                backgroundImage: `url(${image1}) `,
                backgroundPosition: 'center',
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',

            }}

            className="w-[1280px] h-[300px] md:h-[400px] lg:h-[500px] relative align-middle flex items-center justify-center rounded-lg flex-col">
            <h1 className="text-4xl md:text-2xl lg:text-4xl font-bold text-white mb-4 flex items-center justify-center">

                <span className="bg-pink-600 text-2xl mr-4 md:text-5xl lg:text-4xl ">Destination</span>
                Lists
            </h1>
            <p className="text-white font-bold md:text-4xl">Explore the amazing wonders of the world</p>

        </div>
    )
}

export default DestinationHero