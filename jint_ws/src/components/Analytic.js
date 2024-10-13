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

  const [patient, setPatient] = useState(null)
  const [emotionData, setEmotionData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        //const response = await fetch('http://localhost:5000/emotion_data.csv'); // Update with the correct URL to Flask backend
        //if (!response.ok) throw new Error('Network response was not ok');
        
        const { data, error } = await supabase
        .from('user_recordings')
        .select('*')
        .eq('patient_id', 1);

        if (error){

        }else{
          setEmotionData(data[1].recording_session_csv) //Data[n] == Data[user_recording.id]
          const text = emotionData;
          console.log(data)
          console.log(emotionData)

          Papa.parse(emotionData, {
            header: true, // Treat the first row as headers
            dynamicTyping: true, // Automatically convert numbers
            complete: function(results) {
              console.log(results.data); // This will be an array of objects
            },
            error: function(error) {
              console.error('Error parsing CSV:', error);
            }
          });
        }

        //const text = await response.text();
        
        

        
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Emotion Analysis</h2>
      <Line data={chartData} />
    </div>
  );
};

export default Analytic;
