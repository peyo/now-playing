'use client'

import axios from 'axios';
import { Visualizer } from 'react-sound-visualizer';

interface StopButtonProps {
  onStop: () => void;
}

const StopButton = ({ onStop }: StopButtonProps) => {
  const handleClick = async () => {
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
