// PatientPage.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../supabaseClient';

const PatientPage = () => {
  const { id } = useParams(); // Fetch the patient ID from URL params
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    const fetchPatient = async () => {
      const { data, error } = await supabase
        .from('patient')
        .select('*')
        .eq('id', id)
        .single(); // Get a single patient by ID

      if (error) {
        console.error('Error fetching patient:', error);
      } else {
        setPatient(data);
      }
    };

    fetchPatient();
  }, [id]);

  return (
    <div>
      {patient ? (
        <>
          <h1>{patient.name}</h1>
          <p>Patient ID: {patient.id}</p>
          {/* You can add more patient details here */}
        </>
      ) : (
        <p>Loading patient details...</p>
      )}
    </div>
  );
};

export default PatientPage;
