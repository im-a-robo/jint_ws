import './App.css';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import {Video} from './video'

const App = () => {
  return(
    <Router>
        <Routes>
          <Route path='/' element={<Video/>} />
        </Routes>
    </Router>
    );
};


export default App;