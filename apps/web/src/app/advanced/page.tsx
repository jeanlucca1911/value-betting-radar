        } catch (e) {
    console.error(e);
    alert('Failed to load correct scores. Please try again.');
} finally {
    setLoading(false);
}
    };

return (
    <div className="space-y-8">
        <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-slate-100 mb-4">
                Advanced Markets <span className="text-emerald-400">Radar</span>
            </h1>
            <p className="text-slate-400 text-lg">
                Find value in player props, correct scores, and build +EV parlays.
            </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center gap-4 mb-8">
            {/* ... existing tabs ... */}
        </div>

        {/* Content Area */}
        <div className="bg-slate-900/50 border border-slate-700 rounded-2xl p-8 min-h-[400px]">
            {loading && <LoadingSkeleton />}

            {!loading && activeTab === 'props' && (
                <div className="space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-slate-100">Top Player Prop Value</h2>
                        <button
                            onClick={fetchProps}
                            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm text-emerald-400 border border-emerald-500/30"
                        >
                            Refresh Props
                        </button>
                    </div>

                    {props.length === 0 ? (
                        <div className="text-center py-12 text-slate-500">
                            Click refresh to scan for player prop value bets.
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {props.map((prop, i) => (
                                <div key={i} className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-emerald-500/50 transition-all group">
                                    <div className="flex justify-between items-start mb-4">
                                        <div>
                                            <h3 className="font-bold text-lg text-slate-100">{prop.player}</h3>
                                            <p className="text-sm text-slate-400">{prop.team}</p>
                                        </div>
                                        <span className="px-2 py-1 bg-emerald-500/20 text-emerald-400 text-xs rounded border border-emerald-500/30">
                                            +{prop.edge}% Edge
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-end">
                                        <div>
                                            <p className="text-xs text-slate-500 uppercase mb-1">{prop.market}</p>
                                            <p className="text-sm text-slate-300">{prop.bookmaker}</p>
                                        </div>
                                        <div className="text-2xl font-bold text-emerald-400">{prop.odds}</div>
                                    </div>
                                    <button
                                        onClick={() => alert('Parlay Builder coming soon! This will add the bet to your slip.')}
                                        className="w-full mt-4 py-2 bg-emerald-600/10 hover:bg-emerald-600 text-emerald-400 hover:text-white rounded-lg text-sm font-semibold transition-colors"
                                    >
                                        Add to Slip
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {!loading && activeTab === 'scores' && (
                <div className="space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-slate-100">Correct Score Value</h2>
                        <button
                            onClick={fetchScores}
                            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm text-emerald-400 border border-emerald-500/30"
                        >
                            Refresh Scores
                        </button>
                    </div>

                    {scores.length === 0 ? (
                        <div className="text-center py-12 text-slate-500">
                            Click refresh to scan for correct score value bets.
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {scores.map((score, i) => (
                                <div key={i} className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-purple-500/50 transition-all group">
                                    <div className="flex justify-between items-start mb-4">
                                        <div>
                                            <h3 className="font-bold text-3xl text-slate-100">{score.score}</h3>
                                            <p className="text-sm text-slate-400">Exact Score</p>
                                        </div>
                                        <span className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded border border-purple-500/30">
                                            +{score.edge}% Edge
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-end">
                                        <div>
                                            <p className="text-xs text-slate-500 uppercase mb-1">Bookmaker</p>
                                            <p className="text-sm text-slate-300">{score.bookmaker}</p>
                                        </div>
                                        <div className="text-2xl font-bold text-purple-400">{score.odds}</div>
                                    </div>
                                    <button
                                        onClick={() => alert('Parlay Builder coming soon! This will add the bet to your slip.')}
                                        className="w-full mt-4 py-2 bg-purple-600/10 hover:bg-purple-600 text-purple-400 hover:text-white rounded-lg text-sm font-semibold transition-colors"
                                    >
                                        Add to Slip
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {!loading && activeTab === 'parlay' && (
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
        </div>
    </div>
);
}
