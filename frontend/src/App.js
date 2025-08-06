import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [zipFile, setZipFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState('');

  const handleFileChange = e => {
    setZipFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!zipFile) return;
    const formData = new FormData();
    formData.append('file', zipFile);

    const { data } = await axios.post(
      'https://your-backend-url.com/upload',
      formData,
      { responseType: 'blob' }
    );

    const blob = new Blob([data], { type: 'application/zip' });
    const url = window.URL.createObjectURL(blob);
    setDownloadUrl(url);
  };

  return (
    <div className="App">
      <h1>Smart File Organizer</h1>
      <input type="file" accept=".zip" onChange={handleFileChange} />
      <button onClick={handleUpload}>Organize & Download</button>

      {downloadUrl && (
        <a href={downloadUrl} download="organized.zip">
          Download Organized ZIP
        </a>
      )}
    </div>
  );
}

export default App;