import './App.css';
import Map from "./map";

function App() {
  return (
    <>
      {/* Full-screen map container */}
      <div className="map-container">
        <Map />
      </div>
      
      {/* Overlay container for UI elements */}
      <div className="overlay">
        <h1>PintFinder</h1>
        {/* Other overlay content */}
      </div>
    </>
  );
}

export default App;
