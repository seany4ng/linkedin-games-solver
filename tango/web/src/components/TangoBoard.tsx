import React, { useState } from 'react';
import '../styles/TangoBoard.css';
import MoonIcon from '../assets/moon.svg';
import SunIcon from '../assets/sun.svg';
import BlankIcon from '../assets/blank.svg';

const TangoBoard: React.FC = () => {
    // Initialize the board state as a 6x6 grid of blanks
    const [board, setBoard] = useState<string[][]>(
        Array(6).fill(Array(6).fill(''))
    );

    // Cycle through blank -> circle -> X
    const cycleCell = (row: number, col: number) => {
        setBoard((prevBoard) => {
            const newBoard = prevBoard.map((row) => [...row]);
            const currentState = newBoard[row][col];

            newBoard[row][col] =
                currentState === '' ? 'O' : currentState === 'O' ? 'X' : '';
            return newBoard;
        });
    };

    return (
        <div className="tango-board-container">
            {/* Render the board */}
            <div className="board">
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                        {row.map((cell, colIndex) => (
                            <div
                                key={`${rowIndex}-${colIndex}`}
                                className="board-cell"
                                onClick={() => cycleCell(rowIndex, colIndex)}
                            >
                                <div className="board-cell-content">
                                    {
                                        cell === 'O' ? (
                                            <img className="board-cell-img" src={SunIcon} alt="Sun" />
                                        ) : (
                                            cell === 'X' ? <img className="board-cell-img" src={MoonIcon} alt="Moon" />
                                            : (
                                                <img className="board-cell-img"  src={BlankIcon} alt="Blank"/>
                                            )
                                        )
                                    }
                                </div>
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            {/* Render the buttons */}
            <div className="controls">
                <button className="control-button">Undo</button>
                <button className="control-button">Solve</button>
            </div>
        </div>
    );
};

export default TangoBoard;