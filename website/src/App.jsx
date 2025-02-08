// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import Map from './map';
import PubInputPage from './pub_input';

function Home() {
  const navigate = useNavigate();

  return (
    <>

        {/* Overlay container for UI elements */}
        <div className="overlay">
        <h1>PintFinder</h1>
        {/* Button to redirect to the PubInputPage */}
        <button onClick={() => navigate('/pub-input')}>
          Enter Pub Details
        </button>
      </div>


      {/* Full-screen map container */}
      <div className="map-container">
        <Map />
      </div>


    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pub-input" element={<PubInputPage />} />
      </Routes>
    </Router>
  );
}

export default App;
