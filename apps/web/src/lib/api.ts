// Centralized API configuration and fetcher
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://value-betting-radar-production.up.railway.app/api/v1';

console.log('[API Config] API_BASE_URL:', API_BASE_URL);

export async function fetcher(path: string) {
    const url = `${API_BASE_URL}/${path}`;
    console.log('[Fetcher] Fetching URL:', url);

    const res = await fetch(url);

    console.log('[Fetcher] Response status:', res.status);
    console.log('[Fetcher] Response headers:', Object.fromEntries(res.headers.entries()));

    if (!res.ok) {
        const errorText = await res.text();
        console.error('[Fetcher] Error response:', errorText);
        throw new Error(`API Error: ${res.status} - ${errorText}`);
    }

    const data = await res.json();
    console.log('[Fetcher] Response data:', {
        isArray: Array.isArray(data),
        length: Array.isArray(data) ? data.length : 'N/A',
        firstItem: Array.isArray(data) ? data[0] : data,
        data: data
    });

    return data;
}
