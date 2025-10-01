import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';


const Navbar = () => {
  const location = useLocation();
  const [isDestinationsOpen, setIsDestinationsOpen] = useState(false);
  const [isToursOpen, setIsToursOpen] = useState(false);
  const dropdownRef = useRef(null);
  const toursDropdownRef = useRef(null);

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' }
  ];


  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDestinationsOpen(false);
      }
      if (toursDropdownRef.current && !toursDropdownRef.current.contains(event.target)) {
        setIsToursOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <nav className="bg-[#2E2E2E] mt-10 shadow-lg w-[1180px] mx-auto rounded-lg text-white">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-2xl font-allan text-pink-600 hover:text-white transition-colors">
            Travola
          </Link>
          
          <div className="hidden md:flex space-x-8 items-center">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`text-white hover:text-pink-600 transition-colors ${
                  location.pathname === item.path 
                    ? 'text-blue-600 font-semibold' 
                    : ''
                }`}
              >
                {item.name}
              </Link>
            ))}
            
            {/* Destinations Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setIsDestinationsOpen(!isDestinationsOpen)}
                className={`text-white hover:text-pink-600 transition-colors flex items-center space-x-1 ${
                  location.pathname.includes('/destinations') 
                    ? 'text-blue-600 font-semibold' 
                    : ''
                }`}
              >
                <span>Destinations</span>
                <svg 
                  className={`w-4 h-4 transition-transform ${isDestinationsOpen ? 'rotate-180' : ''}`} 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {isDestinationsOpen && (
                <div className="absolute top-full left-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-100 z-50">
                  <Link
                    to="/destinations"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-50 hover:text-pink-600 transition-colors"
                    onClick={() => setIsDestinationsOpen(false)}
                  >
                    All Destinations
                  </Link>
                  <Link
                    to="/destinations/details"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-50 hover:text-pink-600 transition-colors"
                    onClick={() => setIsDestinationsOpen(false)}
                  >
                    Destination Details
                  </Link>
                </div>
              )}
            </div>
            
            {/* Tours Dropdown */}
            <div className="relative" ref={toursDropdownRef}>
              <button
                onClick={() => setIsToursOpen(!isToursOpen)}
                className={`text-white hover:text-pink-600 transition-colors flex items-center space-x-1 ${
                  location.pathname.includes('/tours') 
                    ? 'text-blue-600 font-semibold' 
                    : ''
                }`}
              >
                <span>Tours</span>
                <svg 
                  className={`w-4 h-4 transition-transform ${isToursOpen ? 'rotate-180' : ''}`} 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {isToursOpen && (
                <div className="absolute top-full left-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-100 z-50">
                  <Link
                    to="/tours"
                    className="block px-4 py-2 text-gray-700 hover:bg-pink-50 hover:text-pink-600 transition-colors"
                    onClick={() => setIsToursOpen(false)}
                  >
                    All Tours
                  </Link>
                  <Link
                    to="/tours/details"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                    onClick={() => setIsToursOpen(false)}
                  >
                    Tour Details
                  </Link>
                </div>
              )}
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-gray-700 hover:text-blue-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;