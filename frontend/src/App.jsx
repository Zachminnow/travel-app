import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Destinations from './pages/Destinations';
import DestinationDetails from './pages/DestinationDetails';
import Tours from './pages/Tours';
import TourDetails from './pages/TourDetails';
import About from './pages/About';
import Contact from './pages/Contact';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/destinations" element={<Destinations />} />
          <Route path="/destinations/details" element={<DestinationDetails />} />
          <Route path="/destinations/details/:id" element={<DestinationDetails />} />
          <Route path="/tours" element={<Tours />} />
          <Route path="/tours/details" element={<TourDetails />} />
          <Route path="/tours/details/:id" element={<TourDetails />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
