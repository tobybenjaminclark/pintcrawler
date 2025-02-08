import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Map from "./map"

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app-container">
      <h1>PintFinder</h1>
         <Map />
    </div>
    
    
      
  );
}

export default App
