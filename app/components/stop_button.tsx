'use client'

import axios from 'axios';

const StopButton = () => {
  const handleClick = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/stop');
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
