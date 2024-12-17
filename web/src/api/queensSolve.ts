import { useState } from 'react';
import client from './client'; // Make sure you have a pre-configured Axios client here

// Payload for the queens solve endpoint
interface QueensSolvePayload {
    board: number[][];
}

// Response from the queens solve endpoint
interface QueensSolveResponse {
    solution: number[][]; // 1 for queen, 0 for empty
}

export function useQueensSolve() {
    const [data, setData] = useState<QueensSolveResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<Error | null>(null);

    async function solve(board: number[][]) {
        setLoading(true);
        setError(null);

        try {
            const payload: QueensSolvePayload = { board };
            // POST request to {baseUrl}/queens/solve
            const response = await client.post<QueensSolveResponse>('/queens/solve', payload);

            setData(response.data);
        } catch (err: any) {
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    return { solve, data, loading, error, setData };
}
