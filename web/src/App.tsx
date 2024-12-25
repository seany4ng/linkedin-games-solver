import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './styles/Nav.css';
import LearnPage from './pages/LearnPage';
import PlayPage from './pages/PlayPage';

const App: React.FC = () => {
  return (
    <Router>
      <div>
        {/* Navbar */}
        <nav className="nav">
          <ul className="navbar">
            <li>
              <Link to="/" className="nav-link home-link">
                <img src="/favicon-32x32.png" alt="Home" className="home-icon" />
              </Link>
            </li>
            <li>
              <Link to="/solve" className="nav-link">Learn</Link>
            </li>
            <li>
              <Link to="/play" className="nav-link">Play</Link>
            </li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/solve/*" element={<LearnPage />} />
          <Route path="/play/*" element={<PlayPage />} />
          <Route path="*" element={<div className="placeholder-page">Select a game from the navbar!</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;