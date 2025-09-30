import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-gray-300"> ERROR 404</h1>
          <h2 className="text-3xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
          <p className="text-gray-600 mb-8">
            Oops! It looks like you've wandered off the beaten path. 
            The page you're looking for doesn't exist.
          </p>
        </div>
        
        <div className="space-y-4">
          <Link
            to="/"
            className="inline-block bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Go Back Home
          </Link>
          <br />
          <Link
            to="/destinations"
            className="inline-block text-blue-500 hover:text-blue-600 transition-colors"
          >
            Explore Destinations
          </Link>
        </div>
        
        <div className="mt-12 text-gray-500">
          <p>✈️ Ready to plan your next adventure?</p>
        </div>
      </div>
    </div>
  );
};

export default NotFound;