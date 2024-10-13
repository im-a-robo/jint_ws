import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import Papa from 'papaparse';

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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/emotion_data.csv'); // Update with the correct URL to Flask backend
        if (!response.ok) throw new Error('Network response was not ok');
        
        const text = await response.text();
        
        Papa.parse(text, {
          header: true,
          complete: (results) => {
            console.log('Parsed Results:', results.data); // Check parsed data
            const labels = results.data.map(row => row.timestamp);
            const sad = results.data.map(row => parseFloat(row.sad));
            const angry = results.data.map(row => parseFloat(row.angry));
            const surprise = results.data.map(row => parseFloat(row.surprise));
            const fear = results.data.map(row => parseFloat(row.fear));
            const happy = results.data.map(row => parseFloat(row.happy));
            const disgust = results.data.map(row => parseFloat(row.disgust));
            const neutral = results.data.map(row => parseFloat(row.neutral));

            setChartData({
              labels,
              datasets: [
                { ...chartData.datasets[0], data: sad },
                { ...chartData.datasets[1], data: angry },
                { ...chartData.datasets[2], data: surprise },
                { ...chartData.datasets[3], data: fear },
                { ...chartData.datasets[4], data: happy },
                { ...chartData.datasets[5], data: disgust },
                { ...chartData.datasets[6], data: neutral },
              ],
            });
          },
          error: (error) => {
            console.error('Error parsing CSV:', error);
          },
        });
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
