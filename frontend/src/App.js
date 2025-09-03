import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [captions, setCaptions] = useState([]);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setCaptions([]);
    setCopiedIndex(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://127.0.0.1:8000/generate-caption/', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Failed to generate caption. Please try again.');
      }

      const data = await res.json();
      setCaptions(data.captions);
    } catch (err) {
      console.error('Upload failed:', err);
      setCaptions(['Error generating caption. Please try again.']);
    }

    setLoading(false);
  };

  const handleCopy = (caption, index) => {
    navigator.clipboard.writeText(caption);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 1500);
  };

  const handleTweakCaption = (index) => {
    const newCaption = prompt("Tweak this caption:", captions[index]);
    if (newCaption) {
      const updatedCaptions = [...captions];
      updatedCaptions[index] = newCaption;
      setCaptions(updatedCaptions);
    }
  };

  return (
    <div className="app">
      <h1>Image Caption Generator</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? 'Generating...' : 'Generate Caption'}
      </button>

      {captions.length > 0 && (
        <div className="caption-box">
          <h2>Choose Your Vibe </h2>
          {captions.map((cap, index) => (
            <div key={index} className="caption-option">
              <p>{cap}</p>
              <button onClick={() => handleCopy(cap, index)}>
                {copiedIndex === index ? 'Copied!' : 'Copy'}
              </button>
              <button onClick={() => handleTweakCaption(index)}>Tweak</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
