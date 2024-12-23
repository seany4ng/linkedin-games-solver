import { useState } from 'react';
import client from './client'; // Make sure you have a pre-configured Axios client here

interface TangoGenerateResponse {
    board: string[][],
    row_lines: string[][],
    col_lines: string[][],
    solution: string[][],
}

export function useTangoGenerate() {
    const [data, setData] = useState<TangoGenerateResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<Error | null>(null);

    async function generate(numEqDiff: number) {
        setLoading(true);
        setError(null);

        try {
            const response = await client.get<TangoGenerateResponse>('/tango/generate', {
                params: { num_eq_diff: numEqDiff },
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