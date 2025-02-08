import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);
  const [coordinates, setCoordinates] = useState([-1.1815, 52.947]);
  const [optionVisible, setOptionVisible] = useState(false);

  const locations = [
    { name: "Rose & Crown", coords: [-1.1836073, 52.9476102] },
    { name: "The White Hart", coords: [-1.1793126, 52.9445159] },
    { name: "The Three Wheatsheaves", coords: [-1.1802778, 52.9488889] }
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
      style: "mapbox://styles/mapbox/streets-v11",
      center: coordinates,
      zoom: 15,
    });

    map.on("load", () => {
      map.resize();
      
      locations.forEach((location) => {
        new mapboxgl.Marker()
          .setLngLat(location.coords)
          .setPopup(new mapboxgl.Popup().setText(location.name))
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

    const toggleView = () => {
      setOptionVisible(!optionVisible);
  }

    return () => map.remove();
  }, [coordinates]);

  return <div ref={mapContainerRef} className="map-container"/>;
};

export default Map;
