import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import Papa from 'papaparse';
import { supabase } from '../supabaseClient';

const Analytic = () => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      { label: 'Sad', data: [], borderColor: 'rgba(255, 99, 132, 1)', backgroundColor: 'rgba(255, 99, 132, 0.2)', fill: true },
      { label: 'Angry', data: [], borderColor: 'rgba(54, 162, 235, 1)', backgroundColor: 'rgba(54, 162, 235, 0.2)', fill: true },
      { label: 'Surprise', data: [], borderColor: 'rgba(255, 206, 86, 1)', backgroundColor: 'rgba(255, 206, 86, 0.2)', fill: true },
      { label: 'Fear', data: [], borderColor: 'rgba(75, 192, 192, 1)', backgroundColor: 'rgba(75, 192, 192, 0.2)', fill: true },
      { label: 'Happy', data: [], borderColor: 'rgba(153, 102, 255, 1)', backgroundColor: 'rgba(153, 102, 255, 0.2)', fill: true },
      { label: 'Disgust', data: [], borderColor: 'rgba(255, 159, 64, 1)', backgroundColor: 'rgba(255, 159, 64, 0.2)', fill: true },
      { label: 'Neutral', data: [], borderColor: 'rgba(201, 203, 207, 1)', backgroundColor: 'rgba(201, 203, 207, 0.2)', fill: true },
    ],
  });

  const [patient, setPatient] = useState(null); // To hold the current patient data
  const [emotionData, setEmotionData] = useState(null);
  const PATIENT_ID = 1; // Set the patient ID you want to query

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data, error } = await supabase
          .from('user_recordings')
          .select('*')
          .eq('patient_id', PATIENT_ID); // Using a constant patient ID for querying

        if (error) {
          console.error('Error fetching data:', error);
        } else if (data.length > 0) {
          const csvData = data[3].recording_session_csv; // Use the first item since we are filtering by patient ID
          setEmotionData(csvData); // Set emotion data for parsing

          
          // Parse the CSV
          Papa.parse(csvData, {
            header: true, // Treat the first row as headers
            dynamicTyping: true, // Automatically convert numbers
            complete: function (results) {
              console.log(results.data); // This will be an array of objects

              // Prepare the chart data
              const labels = results.data.map(item => item.timestamp);
              const datasets = chartData.datasets.map(dataset => {
                const emotionKey = dataset.label.toLowerCase();
                return {
                  ...dataset,
                  data: results.data.map(item => item[emotionKey]) // Map emotion values from CSV
                };
              });

              // Update chart data
              setChartData({ labels, datasets });
            },
            error: function (error) {
              console.error('Error parsing CSV:', error);
            }
          });
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    fetchData(); // Fetch data when the component mounts
  }, []); // Empty dependency array ensures it runs only on mount

  return (
    <div>
      <h2>Emotion Analysis</h2>
      <Line data={chartData} />
    </div>
  );
};

export default Analytic;
