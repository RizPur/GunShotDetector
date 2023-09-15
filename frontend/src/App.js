import './App.css';
import React from 'react'
import Appbar from './Components/Appbar';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';

const App = () => {
  const centers =  {ja: [18.19368269899244, -77.39527725784035]};
  const [region, setRegion] = useState(centers.ja);

  const SetMap = () => {
    const map = useMap();
    useEffect(() => {
      map.flyTo(region, 8);
    }, [region, map]);

    return null;
  };

  const flyMap = (x,y) => {
    const newRegion = [x, y]; // new coordinates
    setRegion([18,-77]);
  };

  return (
    <>
      <Appbar flyMap={flyMap} />
      <MapContainer center={centers.ja} zoom={9} style={{width: '100vw', height: '100vh'}} scrollWheelZoom={false} zoomControl={false}> 
        <SetMap />
        <TileLayer
          url="https://api.maptiler.com/maps/basic/256/{z}/{x}/{y}.png?key=73p7aIRQ0vUQYQlwBn1Q"
        />
      </MapContainer>
    </>
  );
}

export default App;
