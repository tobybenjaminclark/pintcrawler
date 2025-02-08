import './App.css';
import Map from "./map2";
import logo from "./assets/logo.png"

function App() {
  return (
    <>
      {/* Full-screen map container */}
      <div className="map-container">
        <Map />
      </div>
      
      {/* Overlay container for UI elements */}
      <div className="overlay">
      <img src={logo} alt="logo" />
        {/* Other overlay content */}
      </div>
    </>
  );
}

export default App;
