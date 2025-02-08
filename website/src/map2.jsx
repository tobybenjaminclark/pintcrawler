import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

// Import the images
import roseAndCrownImg from './assets/rose-and-crown.png';
import whiteHartImg from './assets/white-hart.png';
import threeWheatsheavesImg from './assets/three-wheatsheaves.png';

mapboxgl.accessToken = "pk.eyJ1IjoiYXN3YXJicyIsImEiOiJjbTZ3aGltOTkwZnJxMmlxcTRtemc3aGluIn0.rNpbfxFKGne1I1b6s8uQRQ"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);
  const [coordinates, setCoordinates] = useState([-1.1815, 52.947]);
  const [optionVisible, setOptionVisible] = useState(false);

  // Define locations with images and names
  const locations = [
    { 
      name: "Rose & Crown", 
      coords: [-1.1836073, 52.9476102], 
      image: roseAndCrownImg 
    },
    { 
      name: "The White Hart", 
      coords: [-1.1793126, 52.9445159], 
      image: whiteHartImg 
    },
    { 
      name: "The Three Wheatsheaves", 
      coords: [-1.1802778, 52.9488889], 
      image: threeWheatsheavesImg 
    }
  ];

  const routes = [
    {
      start: "Rose & Crown",
      end: "The Three Wheatsheaves",
      route_coordinates: [
        [-1.1833402, 52.9477021], [-1.1830892, 52.9477336],
        [-1.182844, 52.9476144], [-1.1802856, 52.9485363],
        [-1.1804342, 52.9488203]
      ]
    },
    {
      start: "Rose & Crown",
      end: "The White Hart",
      route_coordinates: [
        [-1.1833402, 52.9477021], [-1.1830892, 52.9477336],
        [-1.182844, 52.9476144], [-1.1834318, 52.9473358],
        [-1.1807212, 52.9462673], [-1.1806955, 52.9453724],
        [-1.1794838, 52.9454115], [-1.1794318, 52.944477]
      ]
    },
    {
      start: "The Three Wheatsheaves",
      end: "The White Hart",
      route_coordinates: [
        [-1.1804342, 52.9488203], [-1.1802856, 52.9485363],
        [-1.1794318, 52.944477]
      ]
    }
  ];

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih",
      center: coordinates,
      zoom: 15,
    });

    map.on("load", () => {
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

      routes.forEach((route, index) => {
        map.addSource(`route-${index}`, {
          type: "geojson",
          data: {
            type: "Feature",
            properties: {},
            geometry: {
              type: "LineString",
              coordinates: route.route_coordinates,
            },
          },
        });

        map.addLayer({
          id: `route-${index}`,
          type: "line",
          source: `route-${index}`,
          layout: { "line-join": "round", "line-cap": "round" },
          paint: { "line-color": "#ff0000", "line-width": 4 },
        });
      });
    });

    return () => map.remove();
  }, [coordinates]);

  // Handle pub click to center map on the selected pub
  const handlePubClick = (coords) => {
    setCoordinates(coords);
  };

  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar or Overlay */}
      <div style={{ width: '250px', padding: '20px', background: '#f0f0f0', height: '100vh', overflowY: 'auto' }}>
        <h2>Nearby Pubs</h2>
        {locations.map((location, index) => (
          <div key={index} style={{ marginBottom: '15px' }}>
            <button 
              onClick={() => handlePubClick(location.coords)}
              style={{
                width: '100%', 
                padding: '10px', 
                textAlign: 'left', 
                backgroundColor: '#fff', 
                border: '1px solid #ddd', 
                borderRadius: '5px', 
                cursor: 'pointer',
                boxShadow: '2px 2px 5px rgba(0,0,0,0.1)'
              }}
            >
              {location.name}
            </button>
          </div>
        ))}
      </div>

      {/* Map Container */}
      <div ref={mapContainerRef} className="map-container" style={{ flex: 1, height: '100vh' }} />
    </div>
  );
};

export default Map;