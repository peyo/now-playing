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

  return <button onClick={handleClick}>Stop</button>;
};

export default StopButton;
