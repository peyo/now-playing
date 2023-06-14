'use client'

import { useContext, useEffect } from 'react';
import axios from 'axios';
import '../globals.css'
import { DataContext } from './dataContext';

const StartButton = () => {
  const { setDataContextValue } = useContext(DataContext);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/check_new_entry');
      const newEntry = response.data.new_entry;
      setDataContextValue(newEntry || ''); // Update the context value
    } catch (error) {
      console.log(error);
    }
  };

  const handleClick = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/start');
      fetchData();
      setInterval(fetchData, 27000);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <div>
        <button onClick={handleClick}>Start</button>
      </div>
    </div>
  );
};

export default StartButton;
