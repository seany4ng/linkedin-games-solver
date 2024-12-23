import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './styles/Nav.css';
import SolvePage from './pages/SolvePage';
import PlayPage from './pages/PlayPage';

const App: React.FC = () => {
  return (
    <Router>
      <div>
        {/* Navbar */}
        <nav>
          <ul className="navbar">
            <li>
              <Link to="/" className="nav-link">Home</Link>
            </li>
            <li>
              <Link to="/solve" className="nav-link">Solve</Link>
            </li>
            <li>
              <Link to="/play" className="nav-link">Play</Link>
            </li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/solve/*" element={<SolvePage />} />
          <Route path="/play/*" element={<PlayPage />} />
          <Route path="*" element={<div className="placeholder-page">Select a game from the navbar!</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;