import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);

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
    new mapboxgl.Marker()
      .setLngLat([-74.5, 40])
      .addTo(map);

    return () => map.remove(); // Cleanup on unmount
  }, []);

  return <div ref={mapContainerRef} className="map-container" />;
};

export default Map;