import React, { useState } from 'react';
import axios from 'axios';
import './AddPill.module.css'

// Define the types for the form fields
interface PillFormData {
  color: string;
  dibujo: string;
  info: string;
  fecha: string;
}

const AddPill: React.FC = () => {
  // State to store form values and errors
  const [formData, setFormData] = useState<PillFormData>({
    color: '',
    dibujo: '',
    info: '',
    fecha: '',
  });

  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.color || !formData.dibujo || !formData.info || !formData.fecha) {
      setError('All fields are required!');
      return;
    }

    try {
      const response = await axios.post('https://your-backend-url/pills', formData, {
        headers: { 'Content-Type': 'application/json' },
      });
      
      setSuccess(response.data.message);
      setError('');

      // Reset the form
      setFormData({
        color: '',
        dibujo: '',
        info: '',
        fecha: '',
      });
    } catch (err) {
      setError('Failed to submit pill data. Please try again.');
      setSuccess('');
    }
  };

  return (
    <div id='wrapper'>
      <h1>Agregar pastilla</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Color</label>
          <input
            type="text"
            name="color"
            value={formData.color}
            onChange={handleInputChange}
          />
        </div>

        <div>
          <label>Dibujo (Pill Name)</label>
          <input
            type="text"
            name="dibujo"
            value={formData.dibujo}
            onChange={handleInputChange}
          />
        </div>

        <div>
          <label>Info</label>
          <textarea
            name="info"
            value={formData.info}
            onChange={handleInputChange}
          />
        </div>

        <div>
          <label>Fecha (Date - dd/mm/yyyy)</label>
          <input
            type="text"
            name="fecha"
            value={formData.fecha}
            onChange={handleInputChange}
            placeholder="dd/mm/yyyy"
          />
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>{success}</p>}

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default AddPill;
