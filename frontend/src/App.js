import './App.css';
import React from 'react'
import Appbar from './Components/Appbar';
import Nav from './Components/Nav';
import GunChart from './Components/GunChart';
import { jaData } from './Data/jaData';
import { MapContainer, TileLayer, useMap, Polygon } from 'react-leaflet';
import { useEffect, useState } from 'react';
import { Box, Modal, Typography, Paper } from '@mui/material';

const centers = {
  ja: [18.19368269899244, -77.39527725784035]
};

const fakeGunShots = [
  {
    ID: 1, prob: 0.7, geo: [18.06840501211612, -77.02277244847099], parish: "CA", "dateTime": "2023-02-27T10:43:00Z", location: "Greater Portmore", probs: {
      AK12: 0.1,
      M4: 0.6,
      IMI: 0.1,
      MP5: 0.2,
      Other: 0
    }
  },
  {
    ID: 2, prob: 0.4, geo: [18.387227121312378, -77.85155660370907], parish: "JM", "dateTime": "2023-09-18T18:05:00Z", location: "Bogue Heights", probs: {
      AK12: 0.1,
      M4: 0.9,
      IMI: 0.0,
      MP5: 0.0,
      Other: 0
    }
  },
  {
    ID: 3, prob: 0.6, geo: [18.037148848846197, -77.29961057965699], parish: "CL", "dateTime": "2023-09-12T11:27:00Z", location: "Hayes", probs: {
      AK12: 0.2,
      M4: 0.1,
      IMI: 0.25,
      MP5: 0.05,
      Other: 0.04
    }
  }

];

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const App = () => {
  const [region, setRegion] = useState(centers.ja);
  const [zoomTo, setZoomTo] = useState(9);
  const [gunShot, setGunShot] = useState({
    ID: 0,
    prob: 0,
    parish: "",
    location: "",
    geo: [0, 0],
    probs: {
      AK12: 0,
      M4: 0,
      IMI: 0,
      MP5: 0,
      Other: 0
    }
  })
  const [gunShots, setGunShots] = useState(fakeGunShots)
  const [show, setShow] = useState(false)

  // useEffect(() => {

  //   const interval = setInterval(() => {
  //     setGunShots(fakeGunShots);
  //   }, 3000);

  //   return () => clearInterval(interval);
  // }, []);


  useEffect(() => {
    const ws = new WebSocket('ws://***.***.**.***:8000/ws/chat/gunsession/');

    ws.onopen = () => {
      console.log('Connected to the WebSocket');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const message = data.message;
      console.log('Received:', message);
    
      if (message && message.geo) {
        const [x, y] = message.geo;
        setGunShot(message)
        // console.log(gunShot)
        flyMap(x, y, 11);
      }
    
      setGunShots(prevGunshots => [...prevGunshots, message]);
      console.log(gunShot,gunShots)
    };
    

    ws.onclose = () => {
      console.log('Disconnected from the WebSocket');
    };

    // Cleanup: close the WebSocket if the component unmounts
    return () => {
      ws.close();
    };
  }, []); // Empty dependency array means this useEffect runs once when the component mounts

  useEffect(() => {
    console.log("Updated gunShot:", gunShot);
  }, [gunShot]);
  
  useEffect(() => {
    console.log("Updated gunShots:", gunShots);
  }, [gunShots]);
  


  const SetMap = () => {
    const map = useMap();
    useEffect(() => {
      map.flyTo(region, zoomTo);
    }, [region, map, zoomTo]);

    return null;
  };

  const flyMap = (x, y, zoom) => {
    setRegion([x, y]);
    setZoomTo(zoom)
  };


  const color = (d) => { //based on amount gunshots
    return d > 5 ? '#800026' :
      // d > 5  ? '#BD0026' :
      d > 2 ? '#E31A1C' :
        // d > 0  ? '#FC4E2A' :
        d > 0 ? '#FD8D3C' :
          // d > 0   ? '#FEB24C' :
          // d > 0   ? '#FED976' :
          '#FFEDA0';
  }
  const getCount = (parishID) => {
    return gunShots.filter((gunShot) => gunShot.parish === parishID).length;
  };


  return (
    <>
      <Appbar flyMap={flyMap} setZoomTo={setZoomTo} setShow={setShow} />
      <Nav setShow={setShow} gunShots={gunShots} setGunShots={setGunShots} setGunShot={setGunShot} flyMap={flyMap} />
      <Modal open={show} onClose={() => { setShow(false) }}>
        <Box style={style}>
          <Paper style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', padding: '20px' }}>
            <GunChart gunShot={gunShot} />
          </Paper>
        </Box>
      </Modal>

      <MapContainer center={centers.ja} zoom={7} style={{ width: '100vw', height: '100vh' }} scrollWheelZoom={false} zoomControl={false}>
        <SetMap zoomTo={zoomTo} />
        <TileLayer
          url="https://api.maptiler.com/maps/basic/256/{z}/{x}/{y}.png?key=73p7aIRQ0vUQYQlwBn1Q"
        />
        {
          jaData.features.map((parish) => {
            const coordinates = parish.geometry.coordinates[0].map((item) => [item[1], item[0]]);
            // console.log(parish.properties.name, coordinates)

            return (
              <Polygon
                pathOptions={{
                  fillColor: color(getCount(parish.id)),
                  fillOpacity: 0.7,
                  weight: 2,
                  opacity: 1,
                  dashArray: 3,
                  color: 'white'
                }}
                positions={coordinates}
                eventHandlers={{
                  mouseover: (e) => {
                    const layer = e.target;
                    layer.setStyle({
                      dashArray: "",
                      fillColor: "#BD0026",
                      fillOpacity: 0.7,
                      weight: 2,
                      opacity: 1,
                      color: "white",
                    })
                  },
                  mouseout: (e) => {
                    const layer = e.target;
                    layer.setStyle({
                      fillOpacity: 0.7,
                      weight: 2,
                      dashArray: "3",
                      color: 'white',
                      fillColor: color(getCount(parish.id)),
                    });
                  },
                  click: (e) => {
                    // setFilterParish('')
                    // setShow(false);
                    console.log("zoom to", parish.id);

                  }
                }}
              />)
          })
        }
      </MapContainer>
    </>
  );
}

export default App;
