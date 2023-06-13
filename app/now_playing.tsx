'use client'

import { useEffect, useState } from 'react';

function NowPlaying() {
  const [trackInfo, setTrackInfo] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchTrackInfo();
  }, []);

  const fetchTrackInfo = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/now_playing');
      if (response.ok) {
        const data = await response.json();
        setTrackInfo(data);
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('Error:', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchButtonClick = () => {
    setLoading(true);
    fetchTrackInfo();
  };

  return (
    <div>
      <h1>Now Playing</h1>
      {loading ? (
        <p>Loading track information...</p>
      ) : (
        <>
          {trackInfo ? (
            <p>{trackInfo}</p>
          ) : (
            <p>No recent tracks found.</p>
          )}
          <button onClick={handleFetchButtonClick}>Start</button>
        </>
      )}
    </div>
  );
}

export default NowPlaying;
