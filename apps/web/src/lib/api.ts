// Centralized API configuration and fetcher
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://value-betting-radar-production.up.railway.app/api/v1';

console.log('[API Config] API_BASE_URL:', API_BASE_URL);

export async function fetcher<T>(path: string): Promise<T> {
    const url = `${API_BASE_URL}/${path}`;
    const requestId = Math.random().toString(36).substring(7);
    console.log(`[Fetcher:${requestId}] Starting request to: ${url}`);

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 15000); // 15s timeout

    try {
        const res = await fetch(url, { signal: controller.signal });
        clearTimeout(id);

        console.log(`[Fetcher:${requestId}] Response status: ${res.status}`);

        if (!res.ok) {
            const errorText = await res.text();
            console.error(`[Fetcher:${requestId}] Error response:`, errorText);
            throw new Error(`API Error: ${res.status} - ${errorText}`);
        }

        return res.json();
    } catch (error) {
        clearTimeout(id);
        console.error(`[Fetcher:${requestId}] Network/Timeout Error:`, error);
        throw error;
    }
}
