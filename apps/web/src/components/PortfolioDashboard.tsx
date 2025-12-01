"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useEffect, useState } from 'react';

interface PortfolioStats {
    total_bets: number;
    settled_bets: number;
    pending_bets: number;
    total_staked: number;
    total_returned: number;
    net_profit: number;
    roi: number;
    win_rate: number;
}

interface DailyProfit {
    date: string;
    profit: number;
    cumulative_profit: number;
}

export function PortfolioDashboard() {
    const [stats, setStats] = useState<PortfolioStats | null>(null);
    const [chartData, setChartData] = useState<DailyProfit[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/bets/stats?user_email=test@example.com')
            .then(res => res.json())
            .then(data => {
                setStats(data.stats);
                setChartData(data.daily_profits);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to load portfolio stats:', err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {[...Array(3)].map((_, i) => (
                    <div key={i} className="bg-slate-800 p-6 rounded-lg border border-slate-700 animate-pulse">
                        <div className="h-4 bg-slate-700 rounded w-24 mb-3"></div>
                        <div className="h-8 bg-slate-700 rounded w-32"></div>
                    </div>
                ))}
            </div>
        );
    }

    if (!stats) {
        return (
            <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 mb-8 text-center text-slate-400">
                No betting history yet. Place some bets to see your stats!
            </div>
        );
    }

    const profitColor = stats.net_profit >= 0 ? 'text-emerald-400' : 'text-red-400';
    const profitSign = stats.net_profit >= 0 ? '+' : '';

    return (
        <div className="space-y-6 mb-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 hover:border-emerald-500/50 transition-colors">
                    <h2 className="text-sm font-medium text-slate-400 uppercase mb-2">Total Profit</h2>
                    <div className={`text-3xl font-bold ${profitColor} mb-1`}>
                        {profitSign}${Math.abs(stats.net_profit).toFixed(2)}
                    </div>
                    <div className="text-xs text-slate-500">
                        {stats.total_bets} bets placed • ${stats.total_staked.toFixed(2)} staked
                    </div>
                </div>

                <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 hover:border-blue-500/50 transition-colors">
                    <h2 className="text-sm font-medium text-slate-400 uppercase mb-2">ROI</h2>
                    <div className={`text-3xl font-bold ${stats.roi >= 0 ? 'text-blue-400' : 'text-red-400'} mb-1`}>
                        {stats.roi >= 0 ? '+' : ''}{stats.roi.toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-500">
                        Return on Investment
                    </div>
                </div>

                <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 hover:border-purple-500/50 transition-colors">
                    <h2 className="text-sm font-medium text-slate-400 uppercase mb-2">Win Rate</h2>
                    <div className="text-3xl font-bold text-purple-400 mb-1">
                        {stats.win_rate.toFixed(1)}%
                    </div>
                    <div className="text-xs text-slate-500">
                        {stats.settled_bets} settled • {stats.pending_bets} pending
                    </div>
                </div>
            </div>

            {/* Chart */}
            {chartData.length > 0 && (
                <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
                    <h2 className="text-lg font-semibold mb-4 text-slate-100">Profit/Loss Over Time</h2>
                    <div className="h-64 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis
                                    dataKey="date"
                                    stroke="#94a3b8"
                                    tick={{ fontSize: 12 }}
                                    tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                                />
                                <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: '#1e293b',
                                        borderColor: '#334155',
                                        color: '#f1f5f9',
                                        borderRadius: '0.5rem'
                                    }}
                                    formatter={(value: number) => [`$${value.toFixed(2)}`, 'Profit']}
                                    labelFormatter={(label) => new Date(label).toLocaleDateString('en-US', {
                                        month: 'long',
                                        day: 'numeric',
                                        year: 'numeric'
                                    })}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="cumulative_profit"
                                    stroke="#10b981"
                                    strokeWidth={3}
                                    dot={{ fill: '#10b981', r: 4 }}
                                    activeDot={{ r: 6 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            )}
        </div>
    );
}
