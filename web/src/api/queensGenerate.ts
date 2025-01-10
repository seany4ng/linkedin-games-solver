import { useState } from 'react';
import client from './client'; // Make sure you have a pre-configured Axios client here

interface QueensGenerateResponse {
    board_size: number;
    board: string[][];
    solution: string[][];
}

export function useQueensGenerate() {
    const [data, setData] = useState<QueensGenerateResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<Error | null>(null);

    async function generate(numRows: number) {
        setLoading(true);
        setError(null);

        try {
            const response = await client.get<QueensGenerateResponse>('/queens/generate', {
                params: { numRows: numRows },
            });
            setData(response.data);
        } catch (err: any) {
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    return { generate, data, loading, error, setData };
}
