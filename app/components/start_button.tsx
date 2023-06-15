'use client'

import { useState, useEffect } from 'react';
import axios from 'axios';
import '../globals.css';

interface StartButtonProps {
  onDataUpdate: (newData: string) => void;
  data: string;
  setAudio: (audio: MediaStream | null) => void;
  setShowVisualizer: (show: boolean) => void;
}

const StartButton = ({ onDataUpdate, data, setAudio, setShowVisualizer }: StartButtonProps) => {

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/check_new_entry');
      const newEntry = response.data.new_entry;
      const dataWithoutTimestamp = removeTimestamp(newEntry?.toString()); // Add null check before calling toString
      console.log(dataWithoutTimestamp)
      onDataUpdate(dataWithoutTimestamp); // Pass the updated data to the parent component
      startDataUpdate(); // Call the function recursively to schedule the subsequent data updates
    } catch (error) {
      console.log(error);
    }
  };

  const handleClick = async () => {
    navigator.mediaDevices
      .getUserMedia({
        audio: true,
        video: false
      })
      .then(setAudio);
    setShowVisualizer(true);

    try {
      await axios.post('http://127.0.0.1:5000/api/start');
      fetchData(); // Call fetchData() once to update the data immediately
    } catch (error) {
      console.log(error);
    }
  };

  const removeTimestamp = (data: string | undefined) => {
    // Assuming the timestamp is in the format "YYYY-MM-DD HH:MM:SS"
    const timestampRegex = /\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/;
    const trimmedData = (data ?? '').replace(timestampRegex, '').trim();
    let result = trimmedData.replace(/^,\s*/, ''); // Remove leading comma and space

    // Remove "None" from the result if it exists
    result = result.replace(/ - None/g, '');
  
    return result;
  };

  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);

  const startDataUpdate = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    const newTimeoutId = setTimeout(() => {
      fetchData();
    }, 27000);
    setTimeoutId(newTimeoutId);
  };

  useEffect(() => {
    fetchData();

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, []);

  return (
    <div>
      <div className="start-button">
        <button onClick={handleClick} className="button-left">
          Start
        </button>
      </div>
    </div>
  );
};

export default StartButton;
