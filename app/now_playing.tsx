'use client'

import { useEffect, useState } from 'react';

function NowPlaying() {
  const [trackInfo, setTrackInfo] = useState<string>('');

  useEffect(() => {
    fetchTrackInfo();
  }, []);

  const fetchTrackInfo = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/track_id');
      if (response.ok) {
        const data = await response.json();
        setTrackInfo(data);
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('Error:', error.message);
    }
  };

  return (
    <div>
      <h1>Now Playing</h1>
      {trackInfo ? (
        <p>{trackInfo}</p>
      ) : (
        <p>Loading track information...</p>
      )}
    </div>
  );
}

export default NowPlaying;
