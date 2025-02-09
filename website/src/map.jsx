import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import DistanceSlider from "./DistanceSlider.jsx";
import { Push } from "./link.jsx";
import MapView from "./MapView.jsx";  // Import the MapView component

const Map = () => {
  const navigate = useNavigate();
  const [coordinates, setCoordinates] = useState([-0.5658, 51.4258]);
  const [overlayVisible, setOverlayVisible] = useState(false);
  const [overlayPosition, setOverlayPosition] = useState({ x: 0, y: 0 });
  const [sliderValue, setSliderValue] = useState(25);
  const [rating, setRating] = useState(-1);
  const [walk, setWalk] = useState(-1);

  const min = () => {
    setRating(0);
  };
  
  const max = () => {
    setRating(1);
  };
  
  const low = () => {
    setWalk(0);
  };
  
  const medium = () => {
    setWalk(1);
  };
  
  const high = () => {
    setWalk(2);
  };

  const send = () => {
    console.log("test");
    console.log(coordinates);
    console.log(Push(coordinates));
    navigate('/Map2'); // Navigate to the new page
  };

  const handleMapClick = (newCoordinates) => {
    setCoordinates(newCoordinates);
    setOverlayPosition({ x: newCoordinates[0], y: newCoordinates[1] });
    setOverlayVisible(true);  // Show the overlay
  };

  return (
    <div className="map-wrapper">
      <MapView coordinates={coordinates} onMapClick={handleMapClick} />

      {overlayVisible && (
        <div className="map-overlay" style={{ top: overlayPosition.y, left: overlayPosition.x }}>
          <div>
            Draft Your Desire   
            <button className="close-button" onClick={() => setOverlayVisible(false)}>X</button>
          </div>
          taverns territory
          <DistanceSlider min={0} max={50} step={0.1} onChange={setSliderValue} />
          Merit of the mead
          <div className="rating">
            <button onClick={min} style={{ backgroundColor: rating === 0 ? '#a4764a' : '' }}>
              Bottom of Barrel
            </button>
            <button onClick={max} style={{ backgroundColor: rating === 1 ? '#d4af37' : '' }}>
              High of Hops
            </button>
          </div>
          Will to Wander
          <div className="rating">
            <button onClick={low} style={{ backgroundColor: walk === 0 ? '#a4764a' : '' }}>
              American
            </button>
            <button onClick={medium} style={{ backgroundColor: walk === 1 ? '#a4764a' : '' }}>
              British
            </button>
            <button onClick={high} style={{ backgroundColor: walk === 2 ? '#d4af37' : '' }}>
              Olympian
            </button>
          </div>
          <div>
            Signed
            <button onClick={send}>...</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Map;
