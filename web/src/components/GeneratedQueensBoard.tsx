import React, { useState, useEffect } from 'react';
import { useQueensGenerate } from '../api/queensGenerate'; // Adjust to your path
import '../styles/GeneratedQueensBoard.css'; // Adjust to your styles
import QueenIcon from '../assets/queen.svg';
import XIcon from '../assets/x.svg';

type Marker = 'none' | 'x' | 'queen';

const GeneratedQueensBoard: React.FC = () => {
    const [boardSize, setBoardSize] = useState<number>(8);
    const [boardColors, setBoardColors] = useState<number[][]>([]);
    const [markerBoard, setMarkerBoard] = useState<Marker[][]>([]);
    const [isMouseDown, setIsMouseDown] = useState<boolean>(false);
    const [timeElapsed, setTimeElapsed] = useState<number>(0);
    const [timerRunning, setTimerRunning] = useState<boolean>(false);
    const [solved, setSolved] = useState<boolean>(false);

    const { generate, data, loading, error, setData } = useQueensGenerate();

    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const size = parseInt(e.target.value, 10);
        setBoardSize(size);
        setSolved(false); // Reset solved state on board size change
    };

    const handleGenerateBoard = async () => {
        await generate(boardSize);
        setSolved(false); // Reset solved state on new board generation
    };

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
    
            setTimeElapsed(0);
            setTimerRunning(true);
        }
    }, [data]);
    
    useEffect(() => {
        let timer: NodeJS.Timeout;
        if (timerRunning) {
            timer = setInterval(() => {
                setTimeElapsed((prev) => prev + 1);
            }, 1000);
        }
        return () => clearInterval(timer);
    }, [timerRunning]);
    

    const handleClear = () => {
        setMarkerBoard((prev) => prev.map((r) => r.map(() => 'none')));
        setSolved(false); // Reset solved state on board clear
    };

    const handleMouseDownOnCell = (row: number, col: number) => {
        if (solved) return;
    
        setIsMouseDown(true);
        setMarkerBoard((prev) => {
            const newMarkers = prev.map((r) => [...r]);
    
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
    
    const handleMouseEnterCell = (row: number, col: number) => {
        if (!isMouseDown || solved) return;
    
        setMarkerBoard((prev) => {
            const newMarkers = prev.map((r) => [...r]);
            if (newMarkers[row][col] === 'none') {
                newMarkers[row][col] = 'x';
            }
            return newMarkers;
        });
    };    

    const handleMouseUp = () => {
        setIsMouseDown(false);
        validateSolution();
    };

    const validateSolution = () => {
        if (!data?.solution) return;
    
        let queensCounter = 0;
        const placedQueens: number[] = [];
        for (let row = 0; row < markerBoard.length; row++) {
            for (let col = 0; col < markerBoard[row].length; col++) {
                if (markerBoard[row][col] === 'queen') {
                    queensCounter++;
                    placedQueens[row] = col;
                }
            }
        }
    
        const isCorrect = 
            queensCounter === boardSize &&
            placedQueens.filter((col) => col !== undefined).length === boardSize &&
            placedQueens.every((col, row) => col === data.solution[row]);
    
        if (isCorrect) {
            setTimerRunning(false);
            setSolved(true);
        }
    };    

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
                <button
                    onClick={handleGenerateBoard}
                    disabled={loading}
                >
                    {loading ? "Generating..." : "Generate Puzzle"}
                </button>
                {error && <div className="error-msg">Error: {error.message}</div>}
            </div>

            {boardColors.length > 0 && 
                <div
                    className="board-grid"
                    onMouseLeave={handleMouseUp}
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

            {boardColors.length > 0 && (
                <div className="bottom-controls">
                    <button onClick={handleClear}>Clear</button>
                    <span className="timer" style={{color:'gray'}}>
                        {Math.floor(timeElapsed / 60)}:{(timeElapsed % 60).toString().padStart(2, '0')}
                    </span>
                    {solved && <span style={{ color: 'green', fontWeight: 'bold' }}>Solved!</span>}
                </div>
            )}
        </div>
    );
};

export default GeneratedQueensBoard;
