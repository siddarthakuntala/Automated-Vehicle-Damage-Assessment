import React, { useState } from 'react';
import './UploadForm.css';

const UploadPage = () => {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!image) return;
    const formData = new FormData();
    formData.append('image', image); // Key must match backend's key

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error processing image');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload a Vehicle Image</h2>

      <label className="custom-file-upload">
        <input type="file" onChange={handleFileChange} />
        Choose Image
      </label>

      {previewUrl && (
        <img className="preview-image" src={previewUrl} alt="Preview" />
      )}

      <button onClick={handleUpload}>Upload</button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <h3>Damage Description:</h3>
          <p>{result.description}</p>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
