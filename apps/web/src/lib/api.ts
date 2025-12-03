// Use environment variable in production, fallback to Railway backend
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://value-betting-radar-production.up.railway.app/api/v1';

export async function fetcher<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}/${path}`);
    if (!res.ok) {
        throw new Error(`An error occurred while fetching the data: ${res.statusText}`);
    }
    return res.json();
}
