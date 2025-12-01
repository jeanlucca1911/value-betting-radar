"use client";

import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer,
    Tooltip,
} from "recharts";
import { ValueBet } from "@/hooks/useLiveOdds";

interface Props {
    bet: ValueBet;
}

export function RadarVisualizer({ bet }: Props) {
    // Normalize metrics to 0-100 scale for the chart
    const data = [
        {
            subject: "Edge",
            A: Math.min(bet.edge * 10, 100), // Scale edge (e.g. 5% -> 50)
            fullMark: 100,
        },
        {
            subject: "Kelly",
            A: Math.min(bet.edge * 5, 100), // Mock Kelly criterion metric
            fullMark: 100,
        },
        {
            subject: "Liquidity",
            A: 80, // Mock liquidity (high for major leagues)
            fullMark: 100,
        },
        {
            subject: "Time",
            A: 90, // Mock time decay (freshness)
            fullMark: 100,
        },
        {
            subject: "Reliability",
            A: bet.bookmaker === "Pinnacle" ? 100 : 70,
            fullMark: 100,
        },
    ];

    return (
        <div className="h-64 w-full bg-slate-800 rounded-lg border border-slate-700 flex flex-col items-center justify-center p-4">
            <h3 className="text-slate-400 text-sm font-medium mb-2">Bet Quality Radar</h3>
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                    <PolarGrid stroke="#475569" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                        name="Metrics"
                        dataKey="A"
                        stroke="#10b981"
                        strokeWidth={2}
                        fill="#10b981"
                        fillOpacity={0.3}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f1f5f9' }}
                        itemStyle={{ color: '#10b981' }}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}
