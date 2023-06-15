'use client'

import axios from 'axios';
import { useState } from "react";
import { Visualizer } from 'react-sound-visualizer';

interface StopButtonProps {
  onStop: () => void;
  setAudio: (audio: MediaStream | null) => void;
  setShowVisualizer: (show: boolean) => void;
}

const StopButton = ({ onStop, setAudio, setShowVisualizer }: StopButtonProps) => {

  const handleClick = async () => {
    setShowVisualizer(false);
    setAudio(null);
    
    try {
      await axios.post('http://127.0.0.1:5000/api/stop');
      onStop(); // Call the onStop function provided as a prop
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="stop-button">
      <button onClick={handleClick} className="button-right">Stop</button>
    </div>
  );
};

export default StopButton;
