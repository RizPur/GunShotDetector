import './App.css';
import React from 'react'
import Appbar from './Components/Appbar';
import Nav from './Components/Nav';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';


const centers =  {
  ja: [18.19368269899244, -77.39527725784035]
};


const App = () => {
  const [region, setRegion] = useState(centers.ja);
  const [gunShot, setGunShot] = useState({
    ID: 0,
    prob : 0,
    parish: "KN",
    location: "RockFort",
    geo: [18, -77],
    probs: {
      AK12 : 0,
      M4: 0,
      IMI: 0,
      MP5: 0,
      Other: 0
    }
  })
  const [gunShots, setGunShots] = useState([])

  useEffect(() => {
    const fakeGunShots = [
      { ID: 1, prob: 0.7, location: "Test1", geo: [18.1, -77.1], probs: { /* ... */ } },
      { ID: 2, prob: 0.4, location: "Test2", geo: [18.2, -77.2], probs: { /* ... */ } },
    ];
  
    // Simulate incoming data every 5 seconds
    const interval = setInterval(() => {
      setGunShots(fakeGunShots);
    }, 5000);
  
    return () => clearInterval(interval);
  }, []);

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
      <Nav gunShots={gunShots} setGunShots={setGunShots} setGunShot={setGunShot}/>
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
