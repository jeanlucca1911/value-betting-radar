'use client';
// Force redeploy: Fix LeagueSelector props mismatch

import { useState, useEffect } from 'react';
import { LeagueSelector } from '@/components/LeagueSelector';
import { fetcher, API_BASE_URL } from '@/lib/api';

interface PropBet {
    player: string;
    team: string;
    market: string;
    odds: number;
    bookmaker: string;
    edge: number;
    match_name: string;
    is_mock?: boolean;
}

interface ScoreBet {
    score: string;
    odds: number;
    bookmaker: string;
    edge: number;
    match_name: string;
    is_mock?: boolean;
}

export default function AdvancedMarketsPage() {
    const [activeTab, setActiveTab] = useState<'props' | 'scores' | 'parlay'>('props');
    const [selectedSport, setSelectedSport] = useState('soccer_epl');
    const [loading, setLoading] = useState(false);
    const [props, setProps] = useState<PropBet[]>([]);
    const [scores, setScores] = useState<ScoreBet[]>([]);

    useEffect(() => {
        async function loadData() {
            setLoading(true);
            try {
                if (activeTab === 'props') {
                    const data = await fetcher(`odds/props?sport=${selectedSport}&region=uk`) as PropBet[];
                    setProps(data);
                } else if (activeTab === 'scores') {
                    const data = await fetcher(`odds/scores?sport=${selectedSport}&region=uk`) as ScoreBet[];
                    setScores(data);
                }
            } catch (error) {
                console.error("Failed to load data", error);
            } finally {
                setLoading(false);
            }
        }

        loadData();
    }, [activeTab, selectedSport]);

    return (
        <div className="min-h-screen bg-slate-900 text-slate-100 p-6">
            <div className="max-w-7xl mx-auto">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400">
                            Advanced Markets
                        </h1>
                        <p className="text-slate-400 mt-2">
                            High-value opportunities in specialized markets.
                        </p>
                    </div>
                    <LeagueSelector
                        currentLeague={selectedSport}
                        onLeagueSelect={setSelectedSport}
                    />
                </div>

                {/* Tabs */}
                <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-xl mb-8 w-fit">
                    <button
                        onClick={() => setActiveTab('props')}
                        className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'props'
                            ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                            }`}
                    >
                        Player Props
                    </button>
                    <button
                        onClick={() => setActiveTab('scores')}
                        className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'scores'
                            ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                            }`}
                    >
                        Correct Score
                    </button>
                    <button
                        onClick={() => setActiveTab('parlay')}
                        className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'parlay'
                            ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                            }`}
                    >
                        Parlay Builder
                    </button>
                </div>

                {/* Content */}
                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
                    </div>
                ) : (
                    <>
                        {activeTab === 'props' && (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {props.map((prop, i) => (
                                    <div key={i} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 hover:border-emerald-500/30 transition-all group">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className="font-bold text-lg text-white group-hover:text-emerald-400 transition-colors">
                                                    {prop.player}
                                                </h3>
                                                <p className="text-sm text-slate-400">{prop.team}</p>
                                                <p className="text-xs text-slate-500 mt-1">{prop.match_name}</p>
                                            </div>
                                            <div className="flex flex-col items-end gap-2">
                                                <span className="px-2 py-1 bg-emerald-500/20 text-emerald-400 text-xs rounded border border-emerald-500/30">
                                                    +{prop.edge}% Edge
                                                </span>
                                                {prop.is_mock && (
                                                    <span className="px-2 py-0.5 bg-blue-500/20 text-blue-400 text-[10px] rounded border border-blue-500/30">
                                                        SIMULATED DATA
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="flex justify-between items-end">
                                            <div>
                                                <p className="text-xs text-slate-500 uppercase mb-1">{prop.market}</p>
                                                <p className="text-sm text-slate-300">{prop.bookmaker}</p>
                                            </div>
                                            <div className="text-2xl font-bold text-emerald-400">{prop.odds}</div>
                                        </div>
                                        <button
                                            onClick={() => alert('Added to slip!')}
                                            className="w-full mt-4 py-2 bg-emerald-600/10 hover:bg-emerald-600 text-emerald-400 hover:text-white rounded-lg text-sm font-semibold transition-colors"
                                        >
                                            Add to Slip
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}

                        {activeTab === 'scores' && (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {scores.map((score, i) => (
                                    <div key={i} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 hover:border-purple-500/30 transition-all group">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className="font-bold text-lg text-white group-hover:text-purple-400 transition-colors">
                                                    {score.score}
                                                </h3>
                                                <p className="text-sm text-slate-400">{score.match_name}</p>
                                            </div>
                                            <div className="flex flex-col items-end gap-2">
                                                <span className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded border border-purple-500/30">
                                                    +{score.edge}% Edge
                                                </span>
                                                {score.is_mock && (
                                                    <span className="px-2 py-0.5 bg-blue-500/20 text-blue-400 text-[10px] rounded border border-blue-500/30">
                                                        SIMULATED DATA
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="flex justify-between items-end">
                                            <div>
                                                <p className="text-xs text-slate-500 uppercase mb-1">Correct Score</p>
                                                <p className="text-sm text-slate-300">{score.bookmaker}</p>
                                            </div>
                                            <div className="text-2xl font-bold text-purple-400">{score.odds}</div>
                                        </div>
                                        <button
                                            onClick={() => alert('Added to slip!')}
                                            className="w-full mt-4 py-2 bg-purple-600/10 hover:bg-purple-600 text-purple-400 hover:text-white rounded-lg text-sm font-semibold transition-colors"
                                        >
                                            Add to Slip
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}

                        {activeTab === 'parlay' && (
                            <div className="text-center py-12">
                                <div className="inline-block p-4 rounded-full bg-slate-800 mb-4">
                                    <svg className="w-12 h-12 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                    </svg>
                                </div>
                                <h3 className="text-xl font-bold text-slate-200 mb-2">Parlay Builder Coming Soon</h3>
                                <p className="text-slate-400 max-w-md mx-auto">
                                    Combine multiple +EV bets to compound your edge. Our algorithm will detect correlated events and calculate the true combined probability.
                                </p>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
