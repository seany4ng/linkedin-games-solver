// src/components/GeneratedTangoBoard.tsx

import React, { useState } from 'react';
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
    // We keep track of the *current* board, vertical lines, horizontal lines,
    // plus the “initial” states that came from generation, so we know how far we can undo/clear.
    const [board, setBoard] = useState<string[][]>([]);
    const [verticalLines, setVerticalLines] = useState<string[][]>([]);
    const [horizontalLines, setHorizontalLines] = useState<string[][]>([]);

    // History is stored for undo, but we also track the index of the
    // earliest history snapshot (the “generated” board).
    const [history, setHistory] = useState<{
        board: string[][][],
        verticalLines: string[][][][],
        horizontalLines: string[][][][]
    }>({ board: [], verticalLines: [], horizontalLines: [] });

    // This index tells us how far back we can undo.
    const [initialHistoryIndex, setInitialHistoryIndex] = useState<number>(0);

    // A separate place to store the solution from the server, if you want
    // to display or otherwise use it.
    const [solution, setSolution] = useState<string[][] | null>(null);

    // ------------------------------------
    // 3. Generate puzzle
    // ------------------------------------
    const handleGeneratePuzzle = async () => {
        // Example:  we pass “numEqDiff” as 8, or allow user to choose it.
        // You can refine this to your app’s needs.
        await generate(8);

        // After `generate(...)` finishes, our `data` prop will be updated.
        // That triggers a re-render, so we can then set states in an effect or right here.
    };

    // If data has changed, we can reflect that in the board
    React.useEffect(() => {
        if (data) {
            // data.board is the 6x6 puzzle
            setBoard(clone2DArray(data.board));

            // For eq/diff lines, you’d likely parse data.eqs / data.diffs
            // exactly how your server returns them. For the sake of example,
            // we’ll assume they are 2D arrays of “=”, “x”, or “ ”, sized
            // properly for vertical/horizontal lines.  If your server returns
            // something else, adjust accordingly:
            setVerticalLines(clone2DArray(data.row_lines));
            setHorizontalLines(clone2DArray(data.col_lines));

            // The solution might also come back in data.solution
            if (data.solution) {
                setSolution(clone2DArray(data.solution));
            }

            // Clear history so that the new puzzle is the earliest state
            const newHistory = {
                board: [],
                verticalLines: [],
                horizontalLines: []
            };
            setHistory(newHistory);
            setInitialHistoryIndex(0);
        }
    }, [data]);

    // ------------------------------------
    // 4. Board interaction
    // ------------------------------------
    const cycleCell = (r: number, c: number) => {
        setBoard(prev => {
            const copy = clone2DArray(prev);
            const current = copy[r][c];
            copy[r][c] = current === ' ' ? 'O' : current === 'O' ? 'X' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleVerticalLine = (r: number, c: number) => {
        setVerticalLines(prev => {
            const copy = clone2DArray(prev);
            const current = copy[r][c];
            copy[r][c] = current === ' ' ? '=' : current === '=' ? 'x' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleHorizontalLine = (r: number, c: number) => {
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
        // Whenever the user changes a cell/line, store a snapshot
        // This effectively pushes the current board state onto the end of the history.
        setHistory(prev => ({
            board: [...prev.board, board],
            verticalLines: [...prev.verticalLines, verticalLines],
            horizontalLines: [...prev.horizontalLines, horizontalLines]
        }));
    };

    const handleUndo = () => {
        // Don’t let the user undo below the “initialHistoryIndex”
        const { board: bHist, verticalLines: vHist, horizontalLines: hHist } = history;
        const lastIndex = bHist.length - 1;
        if (lastIndex >= initialHistoryIndex) {
            // Pop last entry from history
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
                            className={`gen-control-button ${history.board.length <= initialHistoryIndex ? 'disabled' : ''
                                }`}
                            onClick={handleUndo}
                            disabled={history.board.length <= initialHistoryIndex}
                        >
                            Undo
                        </button>

                        <button
                            className={`gen-control-button ${history.board.length <= initialHistoryIndex ? 'disabled' : ''
                                }`}
                            onClick={handleClear}
                            disabled={history.board.length <= initialHistoryIndex}
                        >
                            Clear
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GeneratedTangoBoard;