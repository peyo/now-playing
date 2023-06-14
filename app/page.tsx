'use client'

import React, { useContext } from 'react';
import { DataContext } from './components/dataContext';
import StartButton from './components/startButton';
import StopButton from './components/stopButton';

export default function Page() {
  const { dataContextValue } = useContext(DataContext);

  return (
    <div>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        }}
      >
        <div className="flex space-x-4">
          <StartButton />
          <StopButton />
        </div>
      </div>
      <div style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}>
        <p
          style={{
            animation: 'scrollText 20s linear infinite',
            margin: 0,
            padding: '5px',
          }}
        >
          {dataContextValue || ''}
        </p>
      </div>
    </div>
  );
}
