import React, { useState, useEffect } from 'react';
import { useQueensGenerate } from '../api/queensGenerate'; // Adjust to your path
import '../styles/GeneratedQueensBoard.css'; // Adjust to your styles
import QueenIcon from '../assets/queen.svg';
import XIcon from '../assets/x.svg';

// Define the marker type for each cell
type Marker = 'none' | 'x' | 'queen';

const GeneratedQueensBoard: React.FC = () => {
    const [boardSize, setBoardSize] = useState<number>(8);          // 8 to 10
    const [boardColors, setBoardColors] = useState<number[][]>([]); // 2D array of color indices
    const [markerBoard, setMarkerBoard] = useState<Marker[][]>([]); // 2D array of 'none' | 'x' | 'Q'
    const [isMouseDown, setIsMouseDown] = useState<boolean>(false);

    // Hook to call your backend for generating a new board
    const { generate, data, loading, error, setData } = useQueensGenerate();

    // Update board size from slider
    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const size = parseInt(e.target.value, 10);
        setBoardSize(size);
    };

    // Call backend to generate a new board
    const handleGenerateBoard = async () => {
        await generate(boardSize);
    };

    // Whenever the API hook returns data, set our boardColors & reset markerBoard
    useEffect(() => {
        if (data?.board) {
        const newBoardColors = data.board.map((row) =>
            row.map((val) => parseInt(val, 10))
        );
        setBoardColors(newBoardColors);

        const emptyMarkers: Marker[][] = newBoardColors.map((row) =>
            row.map(() => 'none')
        );
        setMarkerBoard(emptyMarkers);
        }
    }, [data]);

    // Clear everything
    const handleClear = () => {
        setMarkerBoard((prev) => prev.map((r) => r.map(() => 'none')));
    };

    // Mouse-down on a cell → toggle marker
    const handleMouseDownOnCell = (row: number, col: number) => {
        setIsMouseDown(true);

        setMarkerBoard((prev) => {
        const newMarkers = prev.map((r) => [...r]);

        // Toggle logic:
        //   if 'none' → 'x'
        //   else if 'x' → 'Q'
        //   else if 'Q' → do nothing (or revert to 'none' if you prefer)
        if (newMarkers[row][col] === 'none') {
            newMarkers[row][col] = 'x';
        } else if (newMarkers[row][col] === 'x') {
            newMarkers[row][col] = 'queen';
        } else {
            newMarkers[row][col] = 'none';
        }
        return newMarkers;
        });
    };

    // Mouse-enter → paint 'x' if we’re dragging and cell is 'none'
    const handleMouseEnterCell = (row: number, col: number) => {
        if (!isMouseDown) return;

        setMarkerBoard((prev) => {
        const newMarkers = prev.map((r) => [...r]);
        if (newMarkers[row][col] === 'none') {
            newMarkers[row][col] = 'x';
        }
        return newMarkers;
        });
    };

    // Stop dragging
    const handleMouseUp = () => {
        setIsMouseDown(false);
    };

    // Map color indices to actual background colors
    const colorMap = (num: number) => {
        const palette = ['#FE7A60', '#96BEFF', '#B3DFA0', '#E5F387', '#BBA3E2', '#FFC992', '#B9B29E', '#DFDFDF', '#DD9FBA', '#9FD2D5'];
        return palette[num % palette.length] || '#ffffff';
    };

    return (
        <div className="unlimited-queens-container">
            <div className="top-controls">
                <label htmlFor="board-size">Board Size:</label>
                <input
                    id="board-size"
                    type="range"
                    min={7}
                    max={10}
                    value={boardSize}
                    onChange={handleSliderChange}
                />
                <span>{boardSize} x {boardSize}</span>
                <button onClick={handleGenerateBoard}>Generate New Board</button>
            </div>

            {/* Loading / Error Indicators */}
            {loading && <div>Loading…</div>}
            {error && <div style={{ color: 'red' }}>Error: {error.message}</div>}

            {boardColors.length > 0 && 
                <div
                    className="board-grid"
                    onMouseLeave={handleMouseUp} // stop painting if mouse leaves
                >
                    {boardColors.map((row, rIdx) => (
                    <div key={rIdx} className="board-row">
                        {row.map((colorVal, cIdx) => {
                        const backgroundColor = colorMap(colorVal);
                        const marker = markerBoard[rIdx]?.[cIdx];

                        return (
                            <div
                                key={`${rIdx}-${cIdx}`}
                                className="board-cell"
                                style={{ backgroundColor, position: 'relative' }}
                                onMouseDown={() => handleMouseDownOnCell(rIdx, cIdx)}
                                onMouseEnter={() => handleMouseEnterCell(rIdx, cIdx)}
                                onMouseUp={handleMouseUp}
                            >
                            {marker === 'x' && (
                                <img src={XIcon} alt="X" className="marker-icon no-select"/>
                            )}
                            {marker === 'queen' && (
                                <img src={QueenIcon} alt="Q" className="marker-icon no-select" />
                            )}
                            </div>
                        );
                        })}
                    </div>
                    ))}
                </div>
            }
            
            {/* Bottom Controls */}
            {boardColors.length > 0 && (
                <div className="bottom-controls">
                    <button onClick={handleClear}>Clear</button>
                </div>
            )}
        </div>
    );
    };

export default GeneratedQueensBoard;
