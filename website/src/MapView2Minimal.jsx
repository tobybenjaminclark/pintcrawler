// MapView2Minimal.jsx
import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Replace with your Mapbox access token
mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN';

const MapView2Minimal = () => {
  const mapContainerRef = useRef(null);

  useEffect(() => {
    if (!mapContainerRef.current) {
      console.error("Map container ref is null");
      return;
    }
    console.log("Map container ref:", mapContainerRef.current);

    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v11', // Using a default style for testing
      center: [-1.1815, 52.947],
      zoom: 15,
    });

    map.on('load', () => {
      console.log("Map loaded");
      map.resize();
    });

    return () => map.remove();
  }, []);

  return (
    <div
      ref={mapContainerRef}
      style={{ width: '100%', height: '100vh' }} // Fill the viewport
    />
  );
};

export default MapView2Minimal;
