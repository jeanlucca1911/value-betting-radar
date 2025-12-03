// Use environment variable in production, fallback to Railway backend
// Force rebuild: 2024-12-03 13:55
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://value-betting-radar-production.up.railway.app/api/v1';

export async function fetcher<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}/${path}`);
    if (!res.ok) {
        throw new Error(`An error occurred while fetching the data: ${res.statusText}`);
    }
    return res.json();
}
