'use client'

import React, { useState } from 'react';
import StartButton from './components/start_button';
import StopButton from './components/stop_button';
import './globals.css'

export default function Page() {
  const [data, setData] = useState('');

  const onDataUpdate = (newData: string) => {
    setData(newData);
  };

  return (
    <div className="container">
      <div className="box">
        <div className="button-row">
          <StartButton onDataUpdate={onDataUpdate} data={data} />
          <StopButton />
        </div>
        <div className="data-container">
          <p className="scrolling-text">{data}</p> {/* Display the updated data */}
        </div>
      </div>
    </div>
  );
}
