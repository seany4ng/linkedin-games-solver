import React from 'react';
import '../styles/QueensBoard.css'; // Similar to TangoBoard.css but adapted for queens
import QueenIcon from '../assets/queen.svg'; // Provide an icon for the queen, or adjust path

interface SolvedQueensBoardProps {
    solution: number[][] | undefined;
    clearBoard: () => void;
}

const SolvedQueensBoard: React.FC<SolvedQueensBoardProps> = ({ solution, clearBoard }) => {
    if (!solution) {
        return null;
    }

    const BOARD_SIZE = solution.length;

    return (
        <div className="solved-queens-board-container">
            <div className="solved-queens-grid">
                {solution.flatMap((row: number[], rowIndex: number) =>
                    row.map((val, colIndex) => (
                        <div key={`${rowIndex}-${colIndex}`} className="solved-queen-cell">
                            {val === 1 ? <img src={QueenIcon} alt="Q" /> : null}
                        </div>
                    ))
                )}
            </div>
            <div className="controls">
                <button className="control-button" onClick={clearBoard}>
                    Clear Solution
                </button>
            </div>
        </div>
    );
};

export default SolvedQueensBoard;
