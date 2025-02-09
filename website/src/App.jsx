import './App.css';
import Map from "./map";
import logo from "./assets/logo.png"
import useSound from 'use-sound';
import battle from "./assets/battle.mp3"
import { useEffect } from 'react';

const App = () => {
  const [playBattle, { stop, isPlaying }] = useSound(battle, {loop: true});
  
  useEffect(() => {
    playBattle();
    return() => stop();
  }, [playBattle, stop]);
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
