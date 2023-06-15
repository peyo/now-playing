'use client'

import React, { useState, useEffect } from 'react';
import StartButton from './components/start_button';
import StopButton from './components/stop_button';
import { Visualizer } from "react-sound-visualizer";
import './globals.css'

export default function Page() {
  const [data, setData] = useState('');
  const [audio, setAudio] = useState<MediaStream | null>(null);
  const [showVisualizer, setShowVisualizer] = useState(true);
  const mode = "current";

  const onDataUpdate = (newData: string) => {
    setData(newData);
  };

  const handleStop = () => {
    setData(''); // Clear the data by setting it to an empty string
    setShowVisualizer(false);
    if (audio) {
      audio.getTracks().forEach((track) => track.stop());
    }
  };

  const HandleVisualizerReady = (start: () => void) => {
    useEffect(() => {
      if (start) {
        start();
      }
    }, [start]);
  };

  return (
    <div className="container">
      <div className="box">
        <div className="button-row">
          <StartButton onDataUpdate={onDataUpdate} data={data} setAudio={setAudio} setShowVisualizer={setShowVisualizer} />
          <StopButton onStop={handleStop} setAudio={setAudio} setShowVisualizer={setShowVisualizer} />
        </div>
        <div className="data-container">
          <p className="scrolling-text">{data}</p> {/* Display the updated data */}
        </div>
        <div className="visualizer-container">
        {showVisualizer && (
          <Visualizer audio={audio} mode={mode}>
            {({ canvasRef, start }) => {
              HandleVisualizerReady(start ?? (() => {}));
              return (
                <>
                  <canvas ref={canvasRef} width={316} height={100} />
                </>
              );
            }}
          </Visualizer>
        )}
        </div>
      </div>
    </div>
  );
}
