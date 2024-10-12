// Dashboard.js
import React, { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      const therapistId = 1; // Example therapist ID, you can set this dynamically
      const { data, error } = await supabase
        .from('patients')
        .select('*');
        //.eq('therapist_id', therapistId);

      if (error) {
        console.error('Error fetching patients:', error);
      } else {
        setPatients(data);
      }
    };

    fetchPatients();
  }, []);

  console.log(patients);
  
  return (
    <div>
      <h1>Dashboard</h1>
      <ul>
        {patients.map((patient) => (
            <li key={patient.id}> {patient.name} </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
