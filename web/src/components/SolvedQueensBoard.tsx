// import React from 'react';
// import '../styles/SolvedQueensBoard.css'; // Similar to TangoBoard.css but adapted for queens
// import QueenIcon from '../assets/queen.svg'; // Provide an icon for the queen, or adjust path

// interface SolvedQueensBoardProps {
//     solution: number[][] | undefined;
//     clearBoard: () => void;
// }

// const SolvedQueensBoard: React.FC<SolvedQueensBoardProps> = ({ solution, clearBoard }) => {
//     console.log('reached', solution);
//     if (!solution) {
//         return null;
//     }

//     const BOARD_SIZE = solution.length;

//     return (
//         <div className="solved-queens-board-container">
//             <div className="solved-queens-grid">
//                 {solution.flatMap((row: number[], rowIndex: number) =>
//                     row.map((val, colIndex) => (
//                         <div key={`${rowIndex}-${colIndex}`} className="solved-queen-cell">
//                             {val === 1 ? <img src={QueenIcon} alt="Q" /> : null}
//                         </div>
//                     ))
//                 )}
//             </div>
//             <div className="controls">
//                 <button className="control-button" onClick={clearBoard}>
//                     Clear Solution
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default SolvedQueensBoard;


import React from 'react';
import '../styles/SolvedQueensBoard.css';
import QueenIcon from '../assets/queen.svg';

interface SolvedQueensBoardProps {
    solution: number[][] | undefined;
    clearBoard: () => void;
    originalBoard?: string[][]; // Pass in the original board colors
}

const SolvedQueensBoard: React.FC<SolvedQueensBoardProps> = ({ solution, clearBoard, originalBoard }) => {
    if (!solution || !originalBoard) {
        return null;
    }

    const BOARD_SIZE = solution.length;

    return (
        <div className="solved-queens-board-container">
            <div className="solved-board-grid">
                {originalBoard.map((row, rIdx) => (
                    <div key={rIdx} className="board-row">
                        {row.map((cellColor, cIdx) => (
                            <div
                                key={cIdx}
                                className="board-cell solved-board-cell"
                                style={{ backgroundColor: cellColor || 'white' }}
                            >
                                {solution[rIdx][cIdx] === 1 && (
                                    <img src={QueenIcon} alt="Q" className="queen-icon" />
                                )}
                            </div>
                        ))}
                    </div>
                ))}
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