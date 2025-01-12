// src/components/GeneratedTangoBoard.tsx

import React, { useEffect, useState } from 'react';
import '../styles/GeneratedTangoBoard.css';

import MoonIcon from '../assets/moon.svg';
import SunIcon from '../assets/sun.svg';
import BlankIcon from '../assets/blank.svg';

import BlankEqualIcon from '../assets/blank-equal.svg';
import EqualIcon from '../assets/equal.svg';
import DiffIcon from '../assets/diff.svg';

import { useTangoGenerate } from '../api/tangoGenerate';

const BOARD_SIZE = 6;

const GeneratedTangoBoard: React.FC = () => {
    // ------------------------------------
    // 1. Hooks from useTangoGenerate
    // ------------------------------------
    const { generate, data, loading, error, setData } = useTangoGenerate();

    // ------------------------------------
    // 2. Local States
    // ------------------------------------
    const [board, setBoard] = useState<string[][]>([]);
    const [verticalLines, setVerticalLines] = useState<string[][]>([]);
    const [horizontalLines, setHorizontalLines] = useState<string[][]>([]);
    const [isSolved, setIsSolved] = useState<boolean>(false);

    const [history, setHistory] = useState<{
        board: string[][][],
        verticalLines: string[][][][],
        horizontalLines: string[][][][]
    }>({ board: [], verticalLines: [], horizontalLines: [] });

    const [initialHistoryIndex, setInitialHistoryIndex] = useState<number>(0);
    const [solution, setSolution] = useState<string[][] | null>(null);

    // -------------------------------------------------------
    // NEW: Timer states
    // -------------------------------------------------------
    const [time, setTime] = useState<number>(0);
    const [isRunning, setIsRunning] = useState<boolean>(false);

    // -------------------------------------------------------
    // NEW: Track which cells are locked (unmodifiable)
    // -------------------------------------------------------
    const [lockedCells, setLockedCells] = useState<boolean[][]>([]);

    // ------------------------------------
    // 3. Generate puzzle
    // ------------------------------------
    const handleGeneratePuzzle = async () => {
        let numEqDiff = Math.floor(Math.random() * (10 - 4 + 1)) + 4;
        await generate(numEqDiff);
    };

    // If data has changed, reflect it in the board
    useEffect(() => {
        if (data) {
            // 1) set board
            const newBoard = clone2DArray(data.board);
            setBoard(newBoard);

            // 2) set lines
            setVerticalLines(clone2DArray(data.row_lines));
            setHorizontalLines(clone2DArray(data.col_lines));

            // 3) set solution if present
            if (data.solution) {
                setSolution(clone2DArray(data.solution));
            }

            // 4) set locked cells based on original puzzle (anything not blank from the server is locked)
            //    (If you only want O/X locked and ' ' not locked, adjust condition below.)
            const newLockedCells = newBoard.map(row =>
                row.map(cell => cell !== ' ') // lock if not blank
            );
            setLockedCells(newLockedCells);

            // 5) clear history
            const newHistory = {
                board: [],
                verticalLines: [],
                horizontalLines: []
            };
            setHistory(newHistory);
            setInitialHistoryIndex(0);

            // 6) reset and start timer
            setTime(0);
            setIsRunning(true);
        } else {
            // If no puzzle loaded, stop timer and reset time
            setIsRunning(false);
            setTime(0);
        }
    }, [data]);

    // Timer effect: increments every second if `isRunning` is true
    useEffect(() => {
        let intervalId: NodeJS.Timeout | null = null;

        if (isRunning) {
            intervalId = setInterval(() => {
                setTime(prevTime => prevTime + 1);
            }, 1000);
        }
        return () => {
            if (intervalId) clearInterval(intervalId);
        };
    }, [isRunning]);

    // ------------------------------------
    //  Check if solved
    // ------------------------------------
    useEffect(() => {
        const boardFlat = board.flat();
        const solFlat = solution?.flat();
        if (boardFlat.length !== solFlat?.length) {
            setIsSolved(false);
            return;
        }
        if (boardFlat.every((val: string, ind: number) => val === solFlat[ind])) {
            setIsSolved(true);
            // stop timer if puzzle is solved
            setIsRunning(false);
        } else {
            setIsSolved(false);
        }
    }, [board, solution]);

    // ------------------------------------
    // 4. Board interaction
    // ------------------------------------
    const cycleCell = (r: number, c: number) => {
        // Don't allow changes if this cell was part of the original puzzle or puzzle is solved
        if (lockedCells[r]?.[c] || isSolved) return;

        setBoard(prev => {
            const copy = clone2DArray(prev);
            const current = copy[r][c];
            copy[r][c] = current === ' ' ? 'O' : current === 'O' ? 'X' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleVerticalLine = (r: number, c: number) => {
        // If you also want lines to lock after solved, do so here:
        if (isSolved) return;

        setVerticalLines(prev => {
            const copy = clone2DArray(prev);
            const current = copy[r][c];
            copy[r][c] = current === ' ' ? '=' : current === '=' ? 'x' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleHorizontalLine = (r: number, c: number) => {
        // If you also want lines to lock after solved, do so here:
        if (isSolved) return;

        setHorizontalLines(prev => {
            const copy = clone2DArray(prev);
            const current = copy[r][c];
            copy[r][c] = current === ' ' ? '=' : current === '=' ? 'x' : ' ';
            return copy;
        });
        pushHistory();
    };

    // ------------------------------------
    // 5. History management
    // ------------------------------------
    const pushHistory = () => {
        setHistory(prev => ({
            board: [...prev.board, board],
            verticalLines: [...prev.verticalLines, verticalLines],
            horizontalLines: [...prev.horizontalLines, horizontalLines]
        }));
    };

    const handleUndo = () => {
        const { board: bHist, verticalLines: vHist, horizontalLines: hHist } = history;
        const lastIndex = bHist.length - 1;
        if (lastIndex >= initialHistoryIndex) {
            const newBoardHistory = [...bHist];
            const newVerticalHistory = [...vHist];
            const newHorizontalHistory = [...hHist];

            const previousBoard = newBoardHistory.pop()!;
            const previousVertical = newVerticalHistory.pop()!;
            const previousHorizontal = newHorizontalHistory.pop()!;

            setHistory({
                board: newBoardHistory,
                verticalLines: newVerticalHistory,
                horizontalLines: newHorizontalHistory
            });

            setBoard(previousBoard);
            setVerticalLines(previousVertical);
            setHorizontalLines(previousHorizontal);
        }
    };

    const handleClear = () => {
        // Return to the originally generated puzzle
        // i.e., the puzzle state from `data.board` / data.eqs / data.diffs
        if (data) {
            setBoard(clone2DArray(data.board));
            setVerticalLines(clone2DArray(data.row_lines));
            setHorizontalLines(clone2DArray(data.col_lines));
            setHistory({
                board: [],
                verticalLines: [],
                horizontalLines: []
            });
            setInitialHistoryIndex(0);
        }
    };

    // ------------------------------------
    // 6. Helpers
    // ------------------------------------
    const getCellIcon = (val: string) => {
        if (val === 'O') return SunIcon;
        if (val === 'X') return MoonIcon;
        return BlankIcon;
    };

    const getLineIcon = (val: string) => {
        if (val === '=') return EqualIcon;
        if (val === 'x') return DiffIcon;
        return BlankEqualIcon;
    };

    // A quick utility to clone a 2D string array
    const clone2DArray = (arr: string[][]) => arr.map(row => [...row]);

    // Helper to format the timer in m:ss
    const formatTime = (seconds: number) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    // ------------------------------------
    // 7. Render puzzle using an 11×11 grid
    // ------------------------------------
    const GRID_SIZE = 2 * BOARD_SIZE - 1; // for a 6×6 puzzle, that’s 11
    const elements = [];

    for (let gridRow = 0; gridRow < GRID_SIZE; gridRow++) {
        for (let gridCol = 0; gridCol < GRID_SIZE; gridCol++) {
            const isCellPosition = (gridRow % 2 === 0) && (gridCol % 2 === 0);
            const isVerticalLinePosition = (gridRow % 2 === 0) && (gridCol % 2 === 1);
            const isHorizontalLinePosition = (gridRow % 2 === 1) && (gridCol % 2 === 0);
            const isIntersection = (gridRow % 2 === 1) && (gridCol % 2 === 1);

            if (isCellPosition) {
                const cellRow = gridRow / 2;
                const cellCol = gridCol / 2;
                const withinBounds = cellRow < BOARD_SIZE && cellCol < BOARD_SIZE;
                if (withinBounds && board[cellRow]) {
                    const val = board[cellRow][cellCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="generated-cell"
                            onClick={() => cycleCell(cellRow, cellCol)}
                        >
                            <img src={getCellIcon(val)} alt="cell" />
                        </div>
                    );
                } else {
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="generated-filler" />);
                }
            } else if (isVerticalLinePosition) {
                const cellRow = gridRow / 2;
                const lineCol = (gridCol - 1) / 2;
                if (verticalLines[cellRow] && verticalLines[cellRow][lineCol] !== undefined) {
                    const val = verticalLines[cellRow][lineCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="generated-vertical-line"
                        >
                            <img src={getLineIcon(val)} alt="v-line" />
                        </div>
                    );
                } else {
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="generated-filler" />);
                }
            } else if (isHorizontalLinePosition) {
                const lineRow = (gridRow - 1) / 2;
                const cellCol = gridCol / 2;
                if (horizontalLines[lineRow] && horizontalLines[lineRow][cellCol] !== undefined) {
                    const val = horizontalLines[lineRow][cellCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="generated-horizontal-line"
                        >
                            <img src={getLineIcon(val)} alt="h-line" />
                        </div>
                    );
                } else {
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="generated-filler" />);
                }
            } else if (isIntersection) {
                elements.push(
                    <div key={`${gridRow}-${gridCol}`} className="generated-intersection" />
                );
            } else {
                elements.push(<div key={`${gridRow}-${gridCol}`} className="generated-filler" />);
            }
        }
    }

    // ------------------------------------
    // 8. Render
    // ------------------------------------
    return (
        <div className="generated-tango-app-container">
            <div className="generate-section">
                <button
                    className="generate-button"
                    onClick={handleGeneratePuzzle}
                    disabled={loading}
                >
                    {loading ? "Generating..." : "Generate Puzzle"}
                </button>
                {error && <div className="error-msg">Error: {error.message}</div>}
            </div>

            {/* Only show puzzle if we have data */}
            {data && (
                <div className="generated-tango-board-with-lines-container no-select">
                    <div className="generated-puzzle-grid no-select">
                        {elements}
                    </div>

                    <div className="generated-controls no-select">
                        <button
                            className={`gen-control-button ${
                                history.board.length <= initialHistoryIndex ? 'disabled' : ''
                            }`}
                            onClick={handleUndo}
                            disabled={history.board.length <= initialHistoryIndex || isSolved}
                        >
                            Undo
                        </button>

                        <button
                            className={`gen-control-button ${
                                history.board.length <= initialHistoryIndex ? 'disabled' : ''
                            }`}
                            onClick={handleClear}
                            disabled={history.board.length <= initialHistoryIndex || isSolved}
                        >
                            Clear
                        </button>

                        <div style={{color:'gray'}}>
                            {formatTime(time)}
                        </div>

                        {isSolved && <span style={{ color: 'green', fontWeight: 'bold' }}>Solved!</span>}
                    </div>
                </div>
            )}
        </div>
    );
};

export default GeneratedTangoBoard;