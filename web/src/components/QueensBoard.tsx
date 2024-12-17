import React, { useState, useRef } from 'react';
import '../styles/QueensBoard.css';

const MIN_SIZE = 8;
const MAX_SIZE = 10;
const DEFAULT_SIZE = 8;

// Example color palette
const COLORS = ['#FE7A60', '#96BEFF', '#B3DFA0', '#E5F387', '#BBA3E2', '#FFC992', '#B9B29E', '#DFDFDF'];

const QueensBoard: React.FC = () => {
    const [boardSize, setBoardSize] = useState<number>(DEFAULT_SIZE);
    const [board, setBoard] = useState<string[][]>(
        Array.from({ length: DEFAULT_SIZE }, () => Array(DEFAULT_SIZE).fill(''))
    );
    const [selectedColor, setSelectedColor] = useState<string>(COLORS[0]);
    const [isMouseDown, setIsMouseDown] = useState<boolean>(false);

    // Ref to track when user is clicking/dragging on the board
    const boardRef = useRef<HTMLDivElement | null>(null);

    const handleSizeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newSize = parseInt(e.target.value, 10);
        setBoardSize(newSize);
        setBoard(
            Array.from({ length: newSize }, () => Array(newSize).fill(''))
        );
    };

    const handleColorSelect = (color: string) => {
        setSelectedColor(color);
    };

    const paintCell = (row: number, col: number) => {
        setBoard(prev => {
            const copy = prev.map(r => [...r]);
            copy[row][col] = selectedColor;
            return copy;
        });
    };

    const handleMouseDown = (row: number, col: number) => {
        setIsMouseDown(true);
        paintCell(row, col);
    };

    const handleMouseUp = () => {
        setIsMouseDown(false);
    };

    const handleMouseEnter = (row: number, col: number) => {
        if (isMouseDown) {
            paintCell(row, col);
        }
    };

    const handleClear = () => {
        setBoard(Array.from({ length: boardSize }, () => Array(boardSize).fill('')));
    }

    const handleSolve = () => {
        // Placeholder: doesn't do anything yet.
        console.log("Solve button clicked - will integrate later.");
    };

    return (
        <div className="queens-board-container">
            {/* Top Controls: Board Size */}
            <div className="top-controls">
                <label htmlFor="board-size">Board Size:</label>
                <input
                    id="board-size"
                    type="range"
                    min={MIN_SIZE}
                    max={MAX_SIZE}
                    value={boardSize}
                    onChange={handleSizeChange}
                />
                <span>{boardSize} x {boardSize}</span>
            </div>
            
            <div className="main-content">
                {/* Left Column: Color Selection */}
                <div className="color-column">
                    {COLORS.map(color => (
                        <div 
                            key={color} 
                            className={`color-swatch ${color === selectedColor ? 'selected' : ''}`} 
                            style={{ backgroundColor: color }} 
                            onClick={() => handleColorSelect(color)}
                        />
                    ))}
                </div>

                {/* Board Grid */}
                <div 
                    className="board-grid"
                    ref={boardRef}
                    onMouseLeave={handleMouseUp} // stop painting when leaving board
                >
                    {board.map((row, rIdx) => (
                        <div key={rIdx} className="board-row">
                            {row.map((cellColor, cIdx) => (
                                <div
                                    key={cIdx}
                                    className="board-cell"
                                    style={{ backgroundColor: cellColor || 'white' }}
                                    onMouseDown={() => handleMouseDown(rIdx, cIdx)}
                                    onMouseUp={handleMouseUp}
                                    onMouseEnter={() => handleMouseEnter(rIdx, cIdx)}
                                />
                            ))}
                        </div>
                    ))}
                </div>
            </div>

            {/* Bottom Controls: Solve Button */}
            <div className="bottom-controls">
                <button onClick={handleSolve}>Solve</button>
                <button onClick={handleClear}>Clear</button>
            </div>
        </div>
    );
};

export default QueensBoard;
