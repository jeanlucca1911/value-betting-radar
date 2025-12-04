"use client";

import { motion } from "framer-motion";

interface EmptyStateProps {
    sport: string;
    message?: string;
}

export function EmptyState({ sport, message }: EmptyStateProps) {
    const sportNames: Record<string, string> = {
        'soccer_epl': 'Premier League',
        'soccer_uefa_champions_league': 'Champions League',
        'basketball_nba': 'NBA',
        'americanfootball_nfl': 'NFL',
    };

    const sportName = sportNames[sport] || sport;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center py-16 px-4"
        >
            <div className="text-6xl mb-4 opacity-50">📊</div>
            <h3 className="text-xl font-semibold text-gray-300 mb-2">
                No Value Bets Available
            </h3>
            <p className="text-gray-400 text-center max-w-md mb-4">
                {message || `No current value betting opportunities for ${sportName}.`}
            </p>
            <div className="text-sm text-gray-500 text-center mt-4 space-y-1">
                <p>This could mean:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                    <li>Market is very efficient (no +EV opportunities)</li>
                    <li>No upcoming matches in the next 24 hours</li>
                    <li>Games haven't opened betting lines yet</li>
                </ul>
            </div>
            <div className="mt-6 p-4 bg-gray-800/30 rounded-lg border border-gray-700/50">
                <p className="text-xs text-gray-400">
                    💡 <strong>Tip:</strong> Try another sport or check back closer to game time when more bookmakers have set their lines.
                </p>
            </div>
        </motion.div>
    );
}
