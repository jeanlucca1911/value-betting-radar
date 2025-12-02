"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface LeagueSelectorProps {
    selectedLeague: string;
    onSelect: (league: string) => void;
}

const LEAGUES = [
    { id: "soccer_epl", name: "Premier League", icon: "⚽" },
    { id: "soccer_uefa_champs_league", name: "Champions League", icon: "🏆" },
    { id: "basketball_nba", name: "NBA", icon: "🏀" },
    { id: "americanfootball_nfl", name: "NFL", icon: "🏈" },
    { id: "mma_mixed_martial_arts", name: "MMA", icon: "🥊" },
    { id: "tennis_atp_wimbledon", name: "Tennis", icon: "🎾" },
];

export function LeagueSelector({ selectedLeague, onSelect }: LeagueSelectorProps) {
    return (
        <div className="flex flex-wrap gap-2 mb-6">
            {LEAGUES.map((league) => (
                <button
                    key={league.id}
                    onClick={() => onSelect(league.id)}
                    className={cn(
                        "relative px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
                        selectedLeague === league.id
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.2)]"
                            : "bg-slate-800/50 text-slate-400 border-slate-700 hover:bg-slate-800 hover:text-slate-200"
                    )}
                >
                    <span className="mr-2">{league.icon}</span>
                    {league.name}
                    {selectedLeague === league.id && (
                        <motion.div
                            layoutId="activeLeague"
                            className="absolute inset-0 rounded-full border border-emerald-500/50"
                            transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                        />
                    )}
                </button>
            ))}
        </div>
    );
}
