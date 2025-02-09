import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';
import DistanceSlider from "./DistanceSlider.jsx";
import { Push } from "./link.jsx";

mapboxgl.accessToken = "pk.eyJ1IjoiYWxleG5lYWwyMDMwIiwiYSI6ImNtNncycWliNzBiMDAybHNkb3Fma3l1NmcifQ.mvN864hJb5SV2KW6yyYF8g"; // Replace with your token

const Map = () => {
  const mapContainerRef = useRef(null);
  const [coordinates, setCoordinates] = useState([-0.5658, 51.4258]);
  const [overlayVisible, setOverlayVisible] = useState(false);
  const [overlayPosition, setOverlayPosition] = useState({ x: -100, y: -200 });
  const [sliderValue, setSliderValue] = useState(2.5);
  const [rating, setRating] = useState(-1);
  const [walk, setWalk] = useState(-1);
  const [warriorMode, setWarriorMode] = useState(false);
  const [lock, setLock] = useState(false);
  const [description, setDescription] = useState("A brave soul, lucky but special to dare walk the criminal lands");
  const [title, setTitle] = useState("Weakling");

  const min = () => setRating(0);
  const max = () => setRating(1);
  const low = () => setWalk(0);
  const medium = () => setWalk(1);
  const high = () => setWalk(2);

  const WarriorMode = () => {
    setWarriorMode(!warriorMode);
    if (!warriorMode) {
      setDescription("The warrior wanders with immense power, prepared for any challenge that lies ahead!");
      setTitle("A worthy One");
    } else {
      setDescription("A brave soul, lucky but special to dare walk the criminal lands");
      setTitle("Weakling");
    }
  };

  const send = async () => {
    try {
      setLock(true);  // Lock all interactions immediately
      const data = [coordinates[0], coordinates[1], sliderValue, rating, walk, warriorMode];
      console.log("Sending data:", data);

      const response = await Push(data); 
      console.log("Push response:", response);
    } catch (error) {
      console.error("Error in send function:", error);
    } finally {
      setLock(false); // Unlock page after sending data
    }
  };

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/ezequielm/cij7hk832007dapktzdyaemih",
      center: coordinates,
      zoom: 15,
    });

    const handleKeyPress = (event) => {
      if (event.key === 'r' || event.key === 'R') {
        setLock(false);  // Unlock page
      }
    };

    map.on("load", () => {
      map.resize();
    });

    window.addEventListener('keydown', handleKeyPress);

    map.on("click", (event) => {
      if (!lock) {
        event.preventDefault();
        const { lng, lat } = event.lngLat;
        setCoordinates([lng, lat]);

        const canvas = map.getCanvas();
        const rect = canvas.getBoundingClientRect();
        setOverlayVisible(true);
      }
    });

    new mapboxgl.Marker().setLngLat(coordinates).addTo(map);

    return () => map.remove();
  }, [coordinates]);

  return (
    <div className="map-wrapper">
      <div ref={mapContainerRef} className="map-container" />

      {overlayVisible && !lock && (
        <div className="map-overlay" style={{ top: overlayPosition.y, left: overlayPosition.x }}>
          <div>
            Draft Your Desire
            <button className="close-button" onClick={() => setOverlayVisible(false)}>X</button>
          </div>
          taverns territory
          <DistanceSlider min={0} max={5} step={0.1} onChange={setSliderValue} />
          Merit of the mead
          <div className="rating">
            <button onClick={min} style={{ backgroundColor: rating === 0 ? '#a4764a' : '' }}>Bottom of Barrel</button>
            <button onClick={max} style={{ backgroundColor: rating === 1 ? '#d4af37' : '' }}>High of Hops</button>
          </div>
          Will to Wander
          <div className="rating">
            <button onClick={low} style={{ backgroundColor: walk === 0 ? '#a4764a' : '' }}>American</button>
            <button onClick={medium} style={{ backgroundColor: walk === 1 ? '#A6A6A6' : '' }}>British</button>
            <button onClick={high} style={{ backgroundColor: walk === 2 ? '#d4af37' : '' }}>Olympian</button>
          </div>
          <p style={{ fontSize: 25 }}>{title}</p>
          <div className="warrior" style={{ display: 'flex', alignItems: 'center' }}>
            <p1 style={{ marginRight: '10px' }}>{description}</p1>
            <button onClick={WarriorMode} className="special-button" style={{ backgroundColor: warriorMode === true ? '#F00707FF' : '', color: warriorMode ? 'black' : '', border: 'none' }}></button>
          </div>
          <div>
            Signed
            <button onClick={send}>..............</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Map;