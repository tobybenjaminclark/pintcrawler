import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { getCrimesByPoint, plotCrimes } from "./crimeData";

import roseAndCrownImg from "./assets/rose-and-crown.png";

mapboxgl.accessToken = "pk.eyJ1IjoiYXN3YXJicyIsImEiOiJjbTZ3aGltOTkwZnJxMmlxcTRtemc3aGluIn0.rNpbfxFKGne1I1b6s8uQRQ"; // Replace with your Mapbox token

const Map2 = () => {
  const mapContainerRef = useRef(null);
  const [coordinates, setCoordinates] = useState([-1.1815, 52.947]);

  const locations = [
    {
      name: "Rose & Crown",
      coords: [-1.1836073, 52.9476102],
      image: roseAndCrownImg,
    }
  ];

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih",
      center: coordinates,
      zoom: 15,
    });

    map.on("load", async () => {
      map.resize();
      locations.forEach((location) => {
        const popupDiv = document.createElement("div");
        popupDiv.style.textAlign = "center";
        popupDiv.style.maxWidth = "200px";

        const title = document.createElement("h3");
        title.textContent = location.name;
        title.style.marginBottom = "5px";

        const img = document.createElement("img");
        img.src = location.image;
        img.alt = location.name;
        img.style.width = "100%";
        img.style.height = "auto";
        img.style.borderRadius = "5px";
        img.style.boxShadow = "2px 2px 10px rgba(0,0,0,0.3)";

        popupDiv.appendChild(title);
        popupDiv.appendChild(img);

        new mapboxgl.Marker()
          .setLngLat(location.coords)
          .setPopup(new mapboxgl.Popup({ offset: 25 }).setDOMContent(popupDiv))
          .addTo(map);
      });

      // Fetch and plot crimes on the map
      const crimes = await getCrimesByPoint(coordinates[1], coordinates[0]);
      console.log("Fetched crimes:", crimes); 
      if (crimes.length > 0) {
          plotCrimes(map, crimes);
      } else {
          console.log("No crimes found at this location");
    }});

    return () => map.remove();
  }, [coordinates]);

  // Handle pub click to center map on the selected pub
  const handlePubClick = (coords) => {
    setCoordinates(coords);
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

      {/* Map Container */}
      <div
        ref={mapContainerRef}
        className="map-container"
        style={{ flex: 1, height: "100vh" }}
      />
    </div>
  );
};

export default Map2;