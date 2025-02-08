import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);

  const [coordinates, setCoordinates] = useState([1,1]);
  const [beginCoord, setBeginCoord] = useState([-0.5658080564214817,51.42583195427641])
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v11", // Change style as needed
      center: [-0.5658080564214817,51.42583195427641], // [lng, lat]
      zoom: 15,
    });
    map.on("load", () => {
        map.resize();
    })
    
    map.on("click", (event) => {
        event.preventDefault();
        
        setCoordinates([event.lngLat.lat,event.lngLat.lng]);
        console.log([event.lngLat.lat,event.lngLat.lng]);
        console.log(coordinates);
        console.log("test");

    })


    const handleKeyDown = (event) => {
        // Check if the spacebar (key code 32 or key ' ') is pressed
        if (event.key === " ") {
          setran("Spacebar was pressed!");
          console.log(ran);
          console.log("Spacebar was pressed!");
        }
      };
    document.addEventListener("keydown", handleKeyDown);
    new mapboxgl.Marker()
      .setLngLat([-74.5, 40])
      .addTo(map);

    return () => map.remove(); // Cleanup on unmount
  }, [coordinates]);

  return( <div ref={mapContainerRef} className="map-container" />

  )

};

export default Map;