import React, { useState } from 'react';
import '../styles/TangoBoard.css';

import MoonIcon from '../assets/moon.svg';
import SunIcon from '../assets/sun.svg';
import BlankIcon from '../assets/blank.svg';

import BlankEqualIcon from '../assets/blank-equal.svg';
import EqualIcon from '../assets/equal.svg';
import DiffIcon from '../assets/diff.svg';
import { useTangoSolve } from '../api/tangoSolve';

const BOARD_SIZE = 6;

const TangoBoard: React.FC = () => {
    // States
    const [board, setBoard] = useState<string[][]>(
        Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(''))
    );
    const [verticalLines, setVerticalLines] = useState<string[][]>(
        Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE + 1).fill(''))
    );
    const [horizontalLines, setHorizontalLines] = useState<string[][]>(
        Array.from({ length: BOARD_SIZE + 1 }, () => Array(BOARD_SIZE).fill(''))
    );
    const [history, setHistory] = useState<{
        board: string[][][],
        verticalLines: string[][][][],
        horizontalLines: string[][][][]
    }>({ board: [], verticalLines: [], horizontalLines: [] });

    // API (e.g. /tango/solve)
    const { solve, data, loading, error } = useTangoSolve();

    // Helpers
    const cycleCell = (r: number, c: number) => {
        setBoard(prev => {
            const copy = prev.map(row => [...row]);
            const current = copy[r][c];
            copy[r][c] = current === '' ? 'O' : current === 'O' ? 'X' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleVerticalLine = (r: number, c: number) => {
        setVerticalLines(prev => {
            const copy = prev.map(row => [...row]);
            const current = copy[r][c];
            copy[r][c] = current === '' ? '=' : current === '=' ? 'x' : ' ';
            return copy;
        });
        pushHistory();
    };

    const cycleHorizontalLine = (r: number, c: number) => {
        setHorizontalLines(prev => {
            const copy = prev.map(row => [...row]);
            const current = copy[r][c];
            copy[r][c] = current === '' ? '=' : current === '=' ? 'x' : ' ';
            return copy;
        });
        pushHistory();
    };

    const pushHistory = () => {
        setHistory(prev => ({
            board: [...prev.board, board],
            verticalLines: [...prev.verticalLines, verticalLines],
            horizontalLines: [...prev.horizontalLines, horizontalLines]
        }));
    };

    const handleUndo = () => {
        const { board: bHist, verticalLines: vHist, horizontalLines: hHist } = history;
        if (bHist.length > 0) {
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

    const handleSolve = async () => {
        console.log("Logging board:");
        console.log(board);
        console.log("Logging vertical lines:");
        console.log(verticalLines);
        console.log("Logging horizontal lines:");
        console.log(horizontalLines);
        await solve(board, verticalLines, horizontalLines);
        console.log("Logging response data:", data);
    }

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

    // Use an 11x11 grid for a 6x6 board
    const GRID_SIZE = 2 * BOARD_SIZE - 1; // for BOARD_SIZE=6, GRID_SIZE=11

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
                if (withinBounds) {
                    const val = board[cellRow][cellCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="cell"
                            onClick={() => cycleCell(cellRow, cellCol)}
                        >
                            <img src={getCellIcon(val)} alt="cell" />
                        </div>
                    );
                } else {
                    // Should not happen, but if outside puzzle range:
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="filler" />);
                }
            } else if (isVerticalLinePosition) {
                const cellRow = gridRow / 2;
                const lineCol = (gridCol - 1) / 2;
                const withinBounds = cellRow < BOARD_SIZE && lineCol < BOARD_SIZE + 1;
                if (withinBounds) {
                    const val = verticalLines[cellRow][lineCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="vertical-line"
                            onClick={() => cycleVerticalLine(cellRow, lineCol)}
                        >
                            <img src={getLineIcon(val)} alt="v-line" />
                        </div>
                    );
                } else {
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="filler" />);
                }
            } else if (isHorizontalLinePosition) {
                const lineRow = (gridRow - 1) / 2;
                const cellCol = gridCol / 2;
                const withinBounds = lineRow < BOARD_SIZE + 1 && cellCol < BOARD_SIZE;
                if (withinBounds) {
                    const val = horizontalLines[lineRow][cellCol];
                    elements.push(
                        <div
                            key={`${gridRow}-${gridCol}`}
                            className="horizontal-line"
                            onClick={() => cycleHorizontalLine(lineRow, cellCol)}
                        >
                            <img src={getLineIcon(val)} alt="h-line" />
                        </div>
                    );
                } else {
                    elements.push(<div key={`${gridRow}-${gridCol}`} className="filler" />);
                }
            } else if (isIntersection) {
                // Intersection lines inside puzzle
                elements.push(
                    <div key={`${gridRow}-${gridCol}`} className="intersection" />
                );
            } else {
                // Just filler
                elements.push(<div key={`${gridRow}-${gridCol}`} className="filler" />);
            }
        }
    }

    return (
        <div className="tango-board-with-lines-container">
            <div className="puzzle-grid">
                {elements}
            </div>
            <div className="controls">
                <button
                    className={`control-button ${history.board.length === 0 ? 'disabled' : ''}`}
                    onClick={handleUndo}
                    disabled={history.board.length === 0}
                >
                    Undo
                </button>
                <button
                    className="control-button"
                    onClick={handleSolve}
                    disabled={history.board.length === 0}
                >
                    Solve
                </button>
            </div>
        </div>
    );
};

export default TangoBoard;