import useSWR from 'swr';
import { fetcher } from '@/lib/api';

export interface ValueBet {
    match_id: string;
    home_team: string;
    away_team: string;
    commence_time: string;
    bookmaker: string;
    market: string;
    outcome: string;
    odds: number;
    true_probability: number;
    edge: number;
    expected_value: number;
    timestamp: string;
    affiliate_url?: string;
    is_steam_move?: boolean;
    kelly_percentage?: number;
    recommended_stake?: number;
    is_mock?: boolean;
    confidence_grade?: string;
}

export function useLiveOdds(sportKey: string = "soccer_epl", region: string = "uk") {
    console.log('[useLiveOdds] Fetching odds for:', { sportKey, region });

    const { data, error, isLoading } = useSWR<ValueBet[]>(
        `odds/live?sport=${sportKey}&region=${region}`,
        fetcher,
        {
            refreshInterval: 900000, // Poll every 15 minutes
            revalidateOnFocus: false,
            onSuccess: (data) => {
                console.log('[useLiveOdds] SUCCESS - Received data:', {
                    count: data?.length || 0,
                    firstBet: data?.[0],
                    allBets: data
                });
            },
            onError: (err) => {
                console.error('[useLiveOdds] ERROR:', err);
            }
        }
    );

    console.log('[useLiveOdds] Current state:', {
        dataCount: data?.length || 0,
        isLoading,
        error: error?.message,
        data: data
    });

    return {
        data: data || [],
        error,
        isLoading,
    };
}
