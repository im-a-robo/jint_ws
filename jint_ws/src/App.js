import './App.css';
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

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
        setEmotionData((prevData) => ({
          labels: [...prevData.labels, emotions.timestamp],
          datasets: prevData.datasets.map((dataset) => {
            const emotionKey = dataset.label.toLowerCase();
            return {
              ...dataset,
              data: [...dataset.data, emotions[emotionKey]],
            };
          }),
        }));
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
      <header className="top-bar">
        <h1>Emotion Detection</h1>
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
              x: { title: { display: true, text: 'Time' } },
              y: { title: { display: true, text: 'Emotion Confidence (%)' }, min: 0, max: 100 },
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
