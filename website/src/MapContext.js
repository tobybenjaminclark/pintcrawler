import React, { createContext, useContext, useState } from "react";

const MapContext = createContext();

export const useMap = () => {
  return useContext(MapContext);
};

export const MapProvider = ({ children }) => {
  const [mapInstance, setMapInstance] = useState(null);

  return (
    <MapContext.Provider value={{ mapInstance, setMapInstance }}>
      {children}
    </MapContext.Provider>
  );
};
