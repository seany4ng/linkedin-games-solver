import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import TangoBoard from './components/TangoBoard';
import QueensBoard from './components/QueensBoard';
import './styles/Nav.css'; 

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
              <Link to="/tango" className="nav-link">Tango</Link>
            </li>
            <li>
              <Link to="/queens" className="nav-link">Queens</Link>
            </li>
            <li>
              <Link to="/pinpoint" className="nav-link">Pinpoint</Link>
            </li>
            <li>
              <Link to="/crossclimb" className="nav-link">Crossclimb</Link>
            </li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/tango" element={<TangoBoard />} />
          <Route path="/queens" element={<QueensBoard />} />
          <Route path="/pinpoint" element={<div className="placeholder-page">TBD</div>} />
          <Route path="/crossclimb" element={<div className="placeholder-page">TBD</div>} />
          <Route path="*" element={<div className="placeholder-page">Select a game from the navbar!</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
