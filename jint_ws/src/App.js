import './App.css';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import { Video } from './Video';
import { Dashboard } from './components/Dashboard';
import { Patient } from './components/Patient';

const App = () => {
  return (
    <Router>
        <Routes>
        <Route path='/' element={<Dashboard />} />
        <Route path='/patient/:id' element={<Patient />} />
        <Route path='/video' element ={<Video/>}/>
        </Routes>
    </Router>
    );
};


export default App;