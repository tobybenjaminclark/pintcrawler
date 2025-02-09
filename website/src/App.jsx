import './App.css';
import { Routes, Route } from 'react-router-dom'; // Import Routes and Route
import Map from "./map";
import logo from "./assets/logo.png";

// Import NewPage component (Create this if you haven't already)
import Map2 from "./map2"; 

const App = () => {
  return (
    <Routes>
      {/* Define routes for different pages */}
      <Route path="/" element={
        <>
          {/* Full-screen map container */}
          <div className="map-container">
            <Map/>
          </div>

          {/* Overlay container for UI elements */}
          <div className="overlay">
            <img src={logo} alt="logo" />
            {/* Other overlay content */}
          </div>
        </>
      } />
      <Route path="/Map2" element={<Map2 />} /> {/* New page route */}
    </Routes>
  );
}

export default App;
