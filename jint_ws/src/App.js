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
        <h1>Video Stream</h1>
      </header>
      {/* Video Frame */}
      <div className="video-frame">
        {frame && <img src={`data:image/jpeg;base64,${frame}`} alt="Video Frame" />}
      </div>
    </div>
  );
};

export default App;