import logo from './logo.svg';
import './App.css';
import React from 'react'
import { useEffect, useState, useRef } from 'react';
import Appbar from './Components/Appbar';
import Jamaica from './Components/Jamaica';

const centers =  {ja: [18.19368269899244, -77.39527725784035]}

const App = () => {

  return (
    <>
      <Appbar />
      <Jamaica centers={centers}/>
    </>
  );
}

export default App;
