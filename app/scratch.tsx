import { useState, useEffect } from "react";
import { Visualizer } from "react-sound-visualizer";

function App() {
  const [audio, setAudio] = useState<MediaStream | null>(null);
  const [showVisualizer, setShowVisualizer] = useState(true);
  const mode = "current";

  const startAudio = () => {
    navigator.mediaDevices
      .getUserMedia({
        audio: true,
        video: false
      })
      .then(setAudio);
    setShowVisualizer(true);
  };

  const stopAudio = () => {
    if (audio) {
      audio.getTracks().forEach((track) => track.stop());
    }
    setShowVisualizer(false);
  };

  const HandleVisualizerReady = (start: () => void) => {
    useEffect(() => {
      if (start) {
        start();
      }
    }, [start]);
  };

  return (
    <>
      <div>
        <button onClick={startAudio}>Start recording</button>
        <button onClick={stopAudio}>Stop recording</button>
      </div>
      {showVisualizer && (
        <Visualizer audio={audio} mode={mode}>
          {({ canvasRef, start }) => {
            HandleVisualizerReady(start ?? (() => {}));
            return (
              <>
                <canvas ref={canvasRef} width={500} height={100} />
              </>
            );
          }}
        </Visualizer>
      )}
    </>
  );
}

export default App;
