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
    affiliate_url?: string; // Added for monetization
    is_steam_move?: boolean;
}

export function useLiveOdds(sportKey: string = "soccer_epl", region: string = "uk") {
    const { data, error, isLoading } = useSWR<ValueBet[]>(
        `/odds/live?sport=${sportKey}&region=${region}`,
        fetcher,
        {
            refreshInterval: 60000, // Poll every 60 seconds (1 minute)
            revalidateOnFocus: false, // Prevent aggressive refreshing
        }
    );

    return {
        data: data || [],
        error,
        isLoading,
    };
}
