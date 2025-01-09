import React, { useState } from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import '../styles/PlayPage.css';
import GeneratedTangoBoard from '../components/GeneratedTangoBoard';
import GeneratedQueensBoard from '../components/GeneratedQueensBoard';

const PlayPage: React.FC = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const toggleNav = () => {
        setIsCollapsed((prev) => !prev);
    };

    return (
        <div className="solve-page-container">
            <div className="nav-container">
                <aside className={`left-nav ${isCollapsed ? 'collapsed' : ''}`}>
                    <ul>
                        <li>
                            <NavLink
                                to="/play/tango"
                                className={({ isActive }) =>
                                    isActive ? 'solve-nav-link active' : 'solve-nav-link'
                                }
                            >
                                Tango
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/play/queens"
                                className={({ isActive }) =>
                                    isActive ? 'solve-nav-link active' : 'solve-nav-link'
                                }
                            >
                                Queens
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/play/pinpoint"
                                className={({ isActive }) =>
                                    isActive ? 'solve-nav-link active' : 'solve-nav-link'
                                }
                            >
                                Pinpoint
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/play/crossclimb"
                                className={({ isActive }) =>
                                    isActive ? 'solve-nav-link active' : 'solve-nav-link'
                                }
                            >
                                Crossclimb
                            </NavLink>
                        </li>
                    </ul>
                </aside>

                <button className="toggle-button" onClick={toggleNav}>
                    {isCollapsed ? '>' : '<'}
                </button>
            </div>

            <main className="play-content">
                <Routes>
                    <Route path="tango" element={<GeneratedTangoBoard />} />
                    <Route path="queens" element={<GeneratedQueensBoard />} />
                    <Route
                        path="pinpoint"
                        element={
                            <div className="placeholder-page">Pinpoint Page Content TBD</div>
                        }
                    />
                    <Route
                        path="crossclimb"
                        element={
                            <div className="placeholder-page">Crossclimb Page Content TBD</div>
                        }
                    />
                    <Route
                        path="*"
                        element={
                            <div className="placeholder-page">
                                Select a game from the left navbar!
                            </div>
                        }
                    />
                </Routes>
            </main>
        </div>
    );
};

export default PlayPage;