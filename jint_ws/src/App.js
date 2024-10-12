import './App.css';
import React, { useEffect, useState } from 'react';

const App = () => {
  const [frame, setFrame] = useState(null);

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = new WebSocket('ws://localhost:8080');

    socket.onmessage = (event) => {
      const frameData = event.data;
      setFrame(frameData);
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
        <h1>Mood Map</h1>
      </header>
      
      {/* Main Content */}
      <main className="main-content">
        {/* Video Frame */}
        <div className ="emotion-box">Emotions Processor </div>
        <div className="video-frame">
          {frame ? (
            <img src={`data:image/jpeg;base64,${frame}`} alt="Video Frame" className="video-image" />
          ) : (
            <p className="loading-text">Loading video...</p>
          )}
        </div>
        
        {/* Description or Graph Placeholder */}
        <div className="graph-placeholder">
          <h2>Emotion Analysis Graph</h2>
          <p>This area can display graphs or additional information related to the video stream.</p>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="footer">
        <p>© 2024 Therapy Save</p>
      </footer>
    </div>
  );
};

export default App;
