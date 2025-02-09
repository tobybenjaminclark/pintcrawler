import React, { useState } from "react";
import MapView from "./MapView";
import { getCrimesByPoint, plotCrimes } from "./crimeData";
import roseAndCrownImg from "./assets/rose-and-crown.png";

const Map2 = () => {
  const [Coordinates, SetCoordinates] = useState([-1.1815, 52.947]);

  const locations = [
    {
      name: "Rose & Crown",
      coords: [-1.1836073, 52.9476102],
      image: roseAndCrownImg,
    },
  ];

  const handlePubClick = (coords) => {
    SetCoordinates(coords);
  };

  return (
    <div style={{ display: "flex" }}>
      {/* Sidebar or Overlay */}
      <div
        style={{
          width: "250px",
          padding: "20px",
          background: "#f0f0f0",
          height: "100vh",
          overflowY: "auto",
        }}
      >
        <h2>Nearby Pubs</h2>
        {locations.map((location, index) => (
          <div key={index} style={{ marginBottom: "15px" }}>
            <button
              onClick={() => handlePubClick(location.coords)}
              style={{
                width: "100%",
                padding: "10px",
                textAlign: "left",
                backgroundColor: "#fff",
                border: "1px solid #ddd",
                borderRadius: "5px",
                cursor: "pointer",
                boxShadow: "2px 2px 5px rgba(0,0,0,0.1)",
              }}
            >
              {location.name}
            </button>
          </div>
        ))}
      </div>

      {/* Map View Component */}
      <MapView 
        coordinates={Coordinates} 
        onMapClick={SetCoordinates}
        locations={locations} 
        plotCrimes={plotCrimes} 
        getCrimesByPoint={getCrimesByPoint} 
      />
    </div>
  );
};

export default Map2;
