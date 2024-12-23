import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import TangoBoard from '../components/TangoBoard';
import QueensBoard from '../components/QueensBoard';
import '../styles/SolvePage.css';

const SolvePage: React.FC = () => {
    return (
        <div className="solve-page-container">
            <aside className="left-nav">
                <ul>
                    <li>
                        <Link to="/solve/tango" className="solve-nav-link">Tango</Link>
                    </li>
                    <li>
                        <Link to="/solve/queens" className="solve-nav-link">Queens</Link>
                    </li>
                    <li>
                        <Link to="/solve/pinpoint" className="solve-nav-link">Pinpoint</Link>
                    </li>
                    <li>
                        <Link to="/solve/crossclimb" className="solve-nav-link">Crossclimb</Link>
                    </li>
                </ul>
            </aside>
            <main className="main-content">
                <Routes>
                    <Route path="tango" element={<TangoBoard />} />
                    <Route path="queens" element={<QueensBoard />} />
                    <Route path="pinpoint" element={<div className="placeholder-page">Pinpoint Page Content TBD</div>} />
                    <Route path="crossclimb" element={<div className="placeholder-page">Crossclimb Page Content TBD</div>} />
                    <Route path="*" element={<div className="placeholder-page">Select a game from the left navbar!</div>} />
                </Routes>
            </main>
        </div>
    );
};

export default SolvePage;