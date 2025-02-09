import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const MapView = ({ coordinates, onMapClick }) => {
  const mapContainerRef = useRef(null);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih",
      center: coordinates,
      zoom: 15,
    });

    map.on("load", () => {
      map.resize();
    });

    map.on("click", (event) => {
      event.preventDefault();
      const { lng, lat } = event.lngLat;
      onMapClick([lng, lat]);
    });

    new mapboxgl.Marker().setLngLat(coordinates).addTo(map);

    return () => map.remove();
  }, [coordinates, onMapClick]);

  return <div ref={mapContainerRef} className="map-container" />;
};

export default MapView;
