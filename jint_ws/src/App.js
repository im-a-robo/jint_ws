import './App.css';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const MAX_DATA_POINTS = 50; // Set the maximum number of data points

const App = () => {
  const [frame, setFrame] = useState(null);
  const [emotionData, setEmotionData] = useState({
    labels: [], // timestamps
    datasets: [
      { label: 'Sad', data: [], borderColor: 'blue' },
      { label: 'Angry', data: [], borderColor: 'red' },
      { label: 'Surprise', data: [], borderColor: 'orange' },
      { label: 'Fear', data: [], borderColor: 'purple' },
      { label: 'Happy', data: [], borderColor: 'green' },
      { label: 'Disgust', data: [], borderColor: 'brown' },
      { label: 'Neutral', data: [], borderColor: 'grey' },
    ],
  });

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = new WebSocket('ws://localhost:8080');

    socket.onmessage = (event) => {
      try {
        const { frame, emotions } = JSON.parse(event.data);
        setFrame(frame); // Update the video frame

        // Update the emotion data graph
        setEmotionData((prevData) => {
          // Add new timestamp and emotion data
          const newLabels = [...prevData.labels, emotions.timestamp];
          const newDatasets = prevData.datasets.map((dataset) => {
            const emotionKey = dataset.label.toLowerCase();
            return {
              ...dataset,
              data: [...dataset.data, emotions[emotionKey]],
            };
          });

          // Check if the length exceeds the maximum data points
          if (newLabels.length > MAX_DATA_POINTS) {
            newLabels.splice(0, newLabels.length - MAX_DATA_POINTS); // Remove oldest labels
            newDatasets.forEach((dataset) => {
              dataset.data.splice(0, dataset.data.length - MAX_DATA_POINTS); // Remove oldest data
            });
          }

          return {
            labels: newLabels,
            datasets: newDatasets,
          };
        });
      } catch (error) {
        console.error("Error processing WebSocket message:", error);
      }
    };

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    socket.onerror = (error) => {
      console.error("WebSocket error observed:", error);
    };

    // Cleanup function to close the WebSocket connection when the component unmounts
    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();  // Ensure the connection is closed properly
        console.log('WebSocket connection closed on component unmount');
      }
    };
  }, []);

  return (
    <div className="App">
      {/* Top Bar */}
      <h1 className="title">Mood Map</h1>
      <header className="top-bar">
        <h2>Emotion Detection</h2>
      </header>
      {/* Video Frame */}
      <div className="video-frame">
        {frame && <img src={`data:image/jpeg;base64,${frame}`} alt="Video Frame" />}
      </div>
      {/* Line Chart */}
      <div className="chart">
        <Line
          data={emotionData}
          options={{
            scales: {
              x: {
                title: { display: true, text: 'Time' },
                ticks: {
                  autoSkip: true,
                  maxTicksLimit: 5, // Limit the number of ticks on the x-axis
                },
              },
              y: {
                title: { display: true, text: 'Emotion Confidence (%)' },
                min: 0,
                max: 100,
              },
            },
            responsive: true,
            maintainAspectRatio: false,
          }}
        />
      </div>
    </div>
  );
};

export default App;
