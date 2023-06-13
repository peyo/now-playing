'use client'

import { useEffect, useState } from 'react';
import axios from 'axios';

const StartButton = () => {
  const [data, setData] = useState('');

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/check_new_entry');
      const newEntry = response.data.new_entry;
      setData(newEntry || '');
    } catch (error) {
      console.log(error);
    }
  };

  const handleClick = async () => {
    try {
      await axios.post('http://localhost:5000/api/start');
      fetchData();
      setInterval(fetchData, 27000);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div>
      <button onClick={handleClick}>Start</button>
      <p>{data}</p>
    </div>
  );
};

export default StartButton;
