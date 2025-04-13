// pages/index.js
import { useState } from 'react';

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    
    try {
      const res = await fetch('/api/upscale', {
        method: 'POST',
        body: formData
      });
      
      const data = await res.json();
      if(res.ok) {
        setResult(data.hd_image);
      } else {
        alert(data.error);
      }
    } catch (err) {
      alert('Error processing image');
    }
    setLoading(false);
  };

  return (
    <div>
      <h1>Image Upscaler HD</h1>
      <input type="file" onChange={handleUpload} accept="image/*" />
      
      {loading && <p>Processing...</p>}
      
      {result && (
        <div>
          <img src={result} alt="HD Result" style={{maxWidth: '100%'}}/>
          <a href={result} download="hd_image.png">Download HD Image</a>
        </div>
      )}
    </div>
  );
}
