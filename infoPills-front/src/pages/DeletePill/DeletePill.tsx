// src/DeletePill.tsx
import React, { useState } from 'react';
import axios from 'axios';

const DeletePill: React.FC = () => {
  const [color, setColor] = useState<string>('');
  const [dibujo, setDibujo] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.delete('https://your-api-url/pills', {
        data: { color, dibujo },  // Sending `color` and `dibujo` for deletion
      });
      
      setMessage(response.data.message || 'Pill deleted successfully');
      setError('');
      // Reset form
      setColor('');
      setDibujo('');
    } catch (err: any) {
      setMessage('');
      setError('Error deleting pill. Ensure the pill exists.');
    }
  };

  return (
    <div className="form-container">
      <h1>Eliminar pastilla</h1>
      <form onSubmit={handleDelete}>
        <input 
          type="text" 
          placeholder="Enter color" 
          value={color} 
          onChange={(e) => setColor(e.target.value)} 
          required 
        />
        <input 
          type="text" 
          placeholder="Enter dibujo" 
          value={dibujo} 
          onChange={(e) => setDibujo(e.target.value)} 
          required 
        />
        <button type="submit">Delete Pill</button>
      </form>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default DeletePill;
