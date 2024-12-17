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
              <Link to="/tango" className="nav-link">Tango</Link>
            </li>
            <li>
              <Link to="/queens" className="nav-link">Queens</Link>
            </li>
            <li>
              <Link to="/tbd1" className="nav-link">TBD 1</Link>
            </li>
            <li>
              <Link to="/tbd2" className="nav-link">TBD 2</Link>
            </li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/tango" element={<TangoBoard />} />
          <Route path="/queens" element={<QueensBoard />} />
          <Route path="/tbd1" element={<div className="placeholder-page">TBD Page 1</div>} />
          <Route path="/tbd2" element={<div className="placeholder-page">TBD Page 2</div>} />
          <Route path="*" element={<div className="placeholder-page">Select a board from the navbar!</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
