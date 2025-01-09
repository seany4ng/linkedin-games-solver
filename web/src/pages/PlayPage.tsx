import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../styles/PlayPage.css';
import GeneratedTangoBoard from '../components/GeneratedTangoBoard';
import GeneratedQueensBoard from '../components/GeneratedQueensBoard';

const PlayPage: React.FC = () => {
    return (
        <div className="solve-page-container">
            <aside className="left-nav">
                <ul>
                    <li>
                        <Link to="/play/tango" className="solve-nav-link">Tango</Link>
                    </li>
                    <li>
                        <Link to="/play/queens" className="solve-nav-link">Queens</Link>
                    </li>
                    <li>
                        <Link to="/play/pinpoint" className="solve-nav-link">Pinpoint</Link>
                    </li>
                    <li>
                        <Link to="/play/crossclimb" className="solve-nav-link">Crossclimb</Link>
                    </li>
                </ul>
            </aside>
            <main className="play-content">
                <Routes>
                    <Route path="tango" element={<GeneratedTangoBoard />} />
                    <Route path="queens" element={<GeneratedQueensBoard/>} />
                    <Route path="pinpoint" element={<div className="placeholder-page">Pinpoint Page Content TBD</div>} />
                    <Route path="crossclimb" element={<div className="placeholder-page">Crossclimb Page Content TBD</div>} />
                    <Route path="*" element={<div className="placeholder-page">Select a game from the left navbar!</div>} />
                </Routes>
            </main>
        </div>
    );
};

export default PlayPage;