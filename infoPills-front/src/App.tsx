import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Router components
import AddPill from './pages/AddPill/AddPill';
import DeletePill from './pages/DeletePill/DeletePill';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Route for adding a pill */}
          <Route path="/" element={<AddPill />} />

          {/* Route for deleting a pill */}
          <Route path="/delete" element={<DeletePill />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
