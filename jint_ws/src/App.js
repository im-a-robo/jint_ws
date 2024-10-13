import './App.css';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import {Video} from './components/video'
import Analytic from './components/Analytic';

const App = () => {
  return(
    <Router>
      <ul>
        <li>
          <Link to="/analytic">Analysis Chart</Link>
        </li>
        <li>
          <Link to="/">Telehealth Room</Link>
        </li>
      </ul>
        <Routes>
          <Route path='/' element={<Video/>} />
          <Route path='/analytic' element={<Analytic/>} />
        </Routes>
    </Router>
    );
};


export default App;