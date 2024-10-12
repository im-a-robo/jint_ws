import './App.css';
import React, { useEffect, useState } from 'react';

const App = () => {
  const [frame, setFrame] = useState(null);

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = new WebSocket('ws://localhost:8080');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.frame) {
        setFrame(data.frame);
      }
    };

    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => socket.close();
  }, []);

  return (
    <div className="App">
      {/* Top Bar */}
      <header className="top-bar">
        <h1>Therapy Save</h1>
      </header>

      {/* Main Content */}
      <div className="content">
        {/* Left Section: Video Stream */}
        <div className="video-container">
          <h2>Live Stream</h2>
          {frame ? (
            <img src={`data:image/jpeg;base64,${frame}`} alt="Live Video" />
          ) : (
            <p>Loading video...</p>
          )}
        </div>

        {/* Right Section: Graph Placeholder */}
        <div className="graph-container">
          <h2>Graph</h2>
          <div className="graph-placeholder">
            {/* You can replace this placeholder with a real graph later */}
            <p>Graph will appear here.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
