// MapView2.jsx
import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const MapView2 = ({ coordinates, onMapClick, locations, plotCrimes, getCrimesByPoint }) => {
  const mapContainerRef = useRef(null);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih", // Ensure this style URL is valid
      center: coordinates,
      zoom: 15,
    });

    map.on("load", () => {
      map.resize();
    });

    // Optionally add a click handler
    map.on("click", (event) => {
      const { lng, lat } = event.lngLat;
      onMapClick([lng, lat]);
    });

    // Optionally add markers for any provided locations
    if (locations && locations.length > 0) {
      locations.forEach(location => {
        new mapboxgl.Marker()
          .setLngLat(location.coords)
          .addTo(map);
      });
    }

    return () => {
      map.remove();
    };
  }, [coordinates, onMapClick, locations, plotCrimes, getCrimesByPoint]);

  // Use 100% height so it fills the parent container
  return <div ref={mapContainerRef} style={{ width: "100%", height: "100%" }} />;
};

export default MapView2;
