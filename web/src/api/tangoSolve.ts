import { useState } from 'react';
import client from './client'; // Make sure you have a pre-configured Axios client here

interface TangoSolvePayload {
    board: string[][];
    vertical_lines: string[][];
    horizontal_lines: string[][];
}

// Define a type for the response you expect from the server
// This can be adjusted according to the actual response structure.
interface TangoSolveResponse {
    // Example: The solved board might come back as a similar 2D array
    solved_board: string[][];
    // Add other response fields as necessary
}

export function useTangoSolve() {
    const [data, setData] = useState<TangoSolveResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<Error | null>(null);

    async function solve(board: string[][], verticalLines: string[][], horizontalLines: string[][]) {
        setLoading(true);
        setError(null);

        try {
            const payload: TangoSolvePayload = {
                board,
                vertical_lines: verticalLines,
                horizontal_lines: horizontalLines,
            };

            // POST request to {baseUrl}/tango/solve
            const response = await client.post<TangoSolveResponse>('/tango/solve', payload);

            // Update state with the data from the response
            setData(response.data);
        } catch (err: any) {
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    return { solve, data, loading, error, setData };
}