// Centralized API configuration and fetcher
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://value-betting-radar-production.up.railway.app/api/v1';

console.log('[API Config] API_BASE_URL:', API_BASE_URL);

export async function fetcher<T>(path: string): Promise<T> {
    const url = `${API_BASE_URL}/${path}`;

    const res = await fetch(url);

    if (!res.ok) {
        const errorText = await res.text();
        console.error('[Fetcher] Error response:', errorText);
        throw new Error(`API Error: ${res.status} - ${errorText}`);
    }

    return res.json();
}
