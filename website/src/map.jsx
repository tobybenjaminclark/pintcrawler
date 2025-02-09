import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';
import DistanceSlider from "./DistanceSlider.jsx";
import { Push } from "./link.jsx";
import { getCrimesByPoint, plotCrimes } from "./crimeData";
import warriorImg from "./warrior.png";  
import otherImg from "./other.png";      


mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);  // Add a ref to store the map instance
  const [coordinates, setCoordinates] = useState([-0.5658, 51.4258]);
  const [overlayVisible, setOverlayVisible] = useState(false);
  const [overlayPosition, setOverlayPosition] = useState({ x: -100, y: -200 });
  const [sliderValue, setSliderValue] = useState(2.5);
  const [rating, setRating] = useState(0);
  const [walk, setWalk] = useState(0);
  const [warriorMode, setWarriorMode] = useState(false);
  const [lock, setLock] = useState(true);
  const [startPlaced, setStartPlaced] = useState(false);
  const [loading, setLoading] = useState(false); // Loading state for response
  const [routeGenerated, setRouteGenerated] = useState(false); // New state to track if route has been generated
  const [title, setTitle] = useState("Path of the Peacekeeper");
  const [description, setDescription] = useState("Evade Conflict on your path to draughts transcendence.");

  const startPlacedRef = useRef(false); // Use ref instead of state

  const min = () => setRating(0);
  const max = () => setRating(1);
  const low = () => setWalk(0);
  const medium = () => setWalk(1);
  const high = () => setWalk(2);
  const WarriorMode = () => {
    setWarriorMode(!warriorMode);
    if (!warriorMode) {
      setDescription("Fight through land filled with thieves, turmoil, and discord.");
      setTitle("The Warriors Walk");
    } else {
      setDescription("Evade Conflict on your path to draughts transcendence.");
      setTitle("Path of the Peacekeeper");
    }
  };    

  const send = async () => {
    try {
      setRouteGenerated(true);
      setLoading(true); // Set loading to true when awaiting the server response
      setLock(false);
      console.log("test");
      console.log(coordinates);
  
      const data = [coordinates[0], coordinates[1], sliderValue, rating, walk, warriorMode];
  
      console.log("Sending data:", data);
  
      const response = await Push(data); // Await the async function
  
      console.log("Push response:", response);
  
      setLoading(false); // Set loading to false once data is received
  
      // Ensure map is available from the mapRef
      const map = mapRef.current;
  
      // Iterate through each route object in the response.data
      if (response && response.data && Array.isArray(response.data)) {
        response.data.forEach((routeData, index) => {  // Add index parameter
          // Add marker for start node using node.loc
          if (routeData.start_node && Array.isArray(routeData.start_node.loc)) {
            const [lat, lng] = routeData.start_node.loc;
            new mapboxgl.Marker()
              .setLngLat([lng, lat])
              .addTo(map);
          }
  
          // Add marker for end node using node.loc
          if (routeData.end_node && Array.isArray(routeData.end_node.loc)) {
            const [lat, lng] = routeData.end_node.loc;
            new mapboxgl.Marker()
              .setLngLat([lng, lat])
              .addTo(map);
          }
  
          // Add routes between nodes in the response
          if (routeData.route && Array.isArray(routeData.route)) {
            const routeCoordinates = routeData.route.map((point) => {
              if (Array.isArray(point)) {
                const [lat, lng] = point;
                return [lng, lat]; // Use point.loc for each route point
              }
              return [];
            }).filter(coord => coord.length > 0); // Ensure valid coordinates


            // Add route layer with a unique ID based on the index
            map.addSource(`route-${index}`, {
              type: "geojson",
              data: {
                type: "Feature",
                properties: {},
                geometry: {
                  type: "LineString",
                  coordinates: routeCoordinates,
                },
              },
            });
  
            map.addLayer({
              id: `route-${index}`, // Use the index in the ID for uniqueness
              type: "line",
              source: `route-${index}`,
              layout: { "line-join": "round", "line-cap": "round" },
              paint: { "line-color": "#ff0000", "line-width": 4 },
            });
          }
        });
      }
      // Fetch and plot crimes on the map
    const crimes = await getCrimesByPoint(coordinates[1], coordinates[0]);
    console.log("Fetched crimes:", crimes); 
    if (crimes.length > 0) {
        plotCrimes(map, crimes);
    } else {
          console.log("No crimes found at this location");
    };
  
    } catch (error) {
      console.error("Error in send function:", error);
      setLoading(false); // Ensure loading is false in case of an error
    }
  };
  

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih",
      center: coordinates,
      zoom: 15,
    });

    // Store the map instance in the mapRef to make it accessible
    mapRef.current = map;

    map.on("load", () => {
      map.resize();
    });

    map.on("click", async (event) => {
      if (lock && !routeGenerated) {  // Check if route has not been generated
        event.preventDefault();
        const { lng, lat } = event.lngLat;

        console.log(startPlaced)
    
        if (!startPlacedRef.current) {  // Check ref value instead of state
          startPlacedRef.current = true;  // Update the ref directly
    
          new mapboxgl.Marker({ color: 'black' })
            .setLngLat([lng, lat])
            .addTo(map);
        }
    
    
        // Optional: set the coordinates (if you still need them to update)
        // setCoordinates([lng, lat]);
    
        // Get pixel position of click
        const canvas = map.getCanvas();
        const rect = canvas.getBoundingClientRect();
        setOverlayVisible(true);
      }
    });

    return () => map.remove();
  }, [coordinates]);

  return (
    <div className="map-wrapper">
      <div ref={mapContainerRef} className="map-container" />

      {overlayVisible && lock && (
        <div className="map-overlay" style={{ top: overlayPosition.y, left: overlayPosition.x }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
  <p style={{ fontSize: 35, margin: 0 }}>Draft your desire</p>
  <button className="close-button" onClick={() => setOverlayVisible(false)} style={{ border: 'none', background: 'none', fontSize: '25px', cursor: 'pointer' }}>
    X
  </button>
</div>
          <p style={{ fontSize: 25 }}>Taverns Territory</p>
          <DistanceSlider min={0} max={5} step={0.1} onChange={setSliderValue} />
          <p style={{ fontSize: 25 }}>Merit of the mead</p>
          <div className="rating">
            <button onClick={min} style={{ backgroundColor: rating === 0 ? '#a4764a' : '' }}>Bottom of Barrel</button>
            <button onClick={max} style={{ backgroundColor: rating === 1 ? '#d4af37' : '' }}>High of Hops</button>
          </div>
          <p style={{ fontSize: 25 }}>Will to Wander</p>
          <div className="rating">
            <button onClick={low} style={{ backgroundColor: walk === 0 ? '#a4764a' : '' }}>American</button>
            <button onClick={medium} style={{ backgroundColor: walk === 1 ? '#A6A6A6' : '' }}>British</button>
            <button onClick={high} style={{ backgroundColor: walk === 2 ? '#d4af37' : '' }}>Olympian</button>
          </div>
          <p style={{ fontSize: 25 }}>{title}</p>
          <div className="warrior" style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
  <p1 style={{ marginRight: '10px', flex: 1 }}>{description}</p1>
  
  <button
    onClick={WarriorMode}
    className="special-button"
    style={{
      // Make the button square:
      width: "60px",
      height: "60px",

      // Toggle background color based on warriorMode:
      backgroundColor: warriorMode ? "#F00707FF" : "#FFBF00",

      // Square edges and a black border:
      border: "2px solid black",
      borderRadius: 0,  // Ensures no rounded corners

      cursor: "pointer",
      padding: 0  // Ensures no extra space around the image
    }}
  >
    <img
      src={warriorMode ? warriorImg : otherImg}
      alt={warriorMode ? "Warrior Mode" : "Other Mode"}
      style={{
        width: "100%",
        height: "100%",
        objectFit: "cover", // Make the image fill the button
        display: "block"
      }}
    />
  </button>

    </div>
          <div>
            Signed
            <button onClick={send}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};
export default Map;
