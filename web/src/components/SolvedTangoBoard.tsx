import React from 'react';
import '../styles/TangoBoard.css';

import MoonIcon from '../assets/moon.svg';
import SunIcon from '../assets/sun.svg';
import BlankIcon from '../assets/blank.svg';

interface SolvedTangoBoardProps {
    solvedBoard: string[][] | undefined;
    clearBoard: any;
}

const SolvedTangoBoard: React.FC<SolvedTangoBoardProps> = ({ solvedBoard, clearBoard }) => {
    const BOARD_SIZE = 6;

    // Helper to get the corresponding icon for cell values
    const getCellIcon = (val: string) => {
        if (val === 'O') return SunIcon;
        if (val === 'X') return MoonIcon;
        return BlankIcon;
    };

    if (!solvedBoard) {
        return <></>
    }

    return (
        <div className="solved-tango-board-container">
            <div
                className="solved-puzzle-grid"
            >
                {solvedBoard.flatMap((row: string[], rowIndex: number) =>
                    row.map((cell, colIndex) => (
                        <div key={`${rowIndex}-${colIndex}`} className="solved-cell">
                            <img src={getCellIcon(cell)} alt={cell} />
                        </div>
                    ))
                )}
            </div>
            <div className="controls">
                <button
                    className="control-button"
                    onClick={clearBoard}
                >
                    Clear Solution
                </button>
            </div>
        </div>
    );
};

export default SolvedTangoBoard;
