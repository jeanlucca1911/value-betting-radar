import useSWR, { mutate } from 'swr';
import { fetcher, API_BASE_URL } from '@/lib/api';

export interface PortfolioStats {
    total_bets: number;
    settled_bets: number;
    pending_bets: number;
    total_staked: number;
    total_returned: number;
    net_profit: number;
    roi: number;
    win_rate: number;
}

export interface DailyProfit {
    date: string;
    profit: number;
    cumulative_profit: number;
}

interface PortfolioResponse {
    stats: PortfolioStats;
    daily_profits: DailyProfit[];
}

export const PORTFOLIO_STATS_KEY = `bets/stats?user_email=test@example.com`;

export function usePortfolioStats() {
    const { data, error, isLoading } = useSWR<PortfolioResponse>(
        PORTFOLIO_STATS_KEY,
        fetcher
    );

    return {
        stats: data?.stats,
        dailyProfits: data?.daily_profits,
        isLoading,
        error,
        mutate: () => mutate(PORTFOLIO_STATS_KEY)
    };
}
