// LandingPage.tsx
import React from 'react';
import '../styles/LandingPage.css';
import TangoLogo from '../assets/tango_logo.svg';
import QueensLogo from '../assets/queens_logo.svg';
import PinpointLogo from '../assets/pinpoint_logo.svg';
import CrossclimbLogo from '../assets/crossclimb_logo.svg';

const LearnLandingPage: React.FC = () => {
    return (
        <div className="container">
            <div className="title-section">
                <h1 className="title">LinkedIn Games Solver</h1>
                <p className="subtitle">Click any game to start solving!</p>
            </div>

            <div className="tabs">
                <a href="/solve/tango" className="tab">
                    <img src={TangoLogo} alt="Tango" className="tab-logo" />
                    <div>
                        <h3 className="tab-title">Tango</h3>
                        <p className="tab-text">Solve Puzzle</p>
                    </div>
                </a>
                <a href="/solve/queens" className="tab">
                    <img src={QueensLogo} alt="Queens" className="tab-logo" />
                    <div>
                        <h3 className="tab-title">Queens</h3>
                        <p className="tab-text">Solve Puzzle</p>
                    </div>
                </a>
                <a href="/solve/pinpoint" className="tab">
                    <img src={PinpointLogo} alt="Pinpoint" className="tab-logo" />
                    <div>
                        <h3 className="tab-title">Pinpoint</h3>
                        <p className="tab-text">Work In Progress</p>
                    </div>
                </a>
                <a href="/solve/crossclimb" className="tab">
                    <img src={CrossclimbLogo} alt="Crossclimb" className="tab-logo" />
                    <div>
                        <h3 className="tab-title">Crossclimb</h3>
                        <p className="tab-text">Work In Progress</p>
                    </div>
                </a>
            </div>
        </div>
    );
};

export default LearnLandingPage;
