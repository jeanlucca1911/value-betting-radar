"use client";

import { useState, Fragment } from "react";
import { ValueBet } from "@/hooks/useLiveOdds";
import { RadarVisualizer } from "./RadarVisualizer";
import { API_BASE_URL } from "@/lib/api";

interface Props {
  bets: ValueBet[];
  lastUpdate?: Date;
}

export function OddsTable({ bets, lastUpdate }: Props) {
  const [expandedBetId, setExpandedBetId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedBetId(expandedBetId === id ? null : id);
  };

  const placeBet = async (bet: ValueBet) => {
    try {
      const res = await fetch(`${API_BASE_URL}/bets/place`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          match_id: bet.match_id,
          home_team: bet.home_team,
          away_team: bet.away_team,
          selection: bet.outcome,
          odds: bet.odds,
          stake: 100,
          bookmaker: bet.bookmaker,
          edge: bet.edge,
        }),
      });
      if (res.ok) {
        alert(`Bet tracked! ${bet.outcome} @ ${bet.odds}`);
      } else {
        alert("Failed to track bet");
      }
    } catch (e) {
      console.error(e);
      alert("Error tracking bet");
    }
  };

  const getEdgeColor = (edge: number) => {
    if (edge >= 5) return "text-emerald-400";
    if (edge >= 2) return "text-yellow-400";
    return "text-orange-400";
  };

  const getEdgeBadge = (edge: number) => {
    if (edge >= 5) return { text: "Strong", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" };
    if (edge >= 2) return { text: "Moderate", color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30" };
    return { text: "Weak", color: "bg-orange-500/20 text-orange-400 border-orange-500/30" };
  };

  return (
    <div className="space-y-4">
      {/* Header with last update */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-xl font-bold text-slate-100">Live Value Bets</h2>
          <span className="px-3 py-1 text-xs bg-emerald-500/20 text-emerald-400 rounded-full border border-emerald-500/30 flex items-center gap-2">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
            {bets.length} Opportunities
          </span>
        </div>
        {lastUpdate && (
          <div className="text-sm text-slate-500">
            Updated {new Date(lastUpdate).toLocaleTimeString()}
          </div>
        )}
      </div>

      {/* Trust badge */}
      <div className="flex items-center gap-2 text-xs text-slate-500 pb-2">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <span>Powered by The Odds API • Updated every 30 seconds</span>
      </div>

      <div className="overflow-x-auto rounded-lg border border-slate-700 shadow-xl">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="bg-slate-800 text-xs uppercase text-slate-400 border-b border-slate-700">
            <tr>
              <th className="px-6 py-4 font-semibold">Match</th>
              <th className="px-6 py-4 font-semibold">Time</th>
              <th className="px-6 py-4 font-semibold">Bookmaker</th>
              <th className="px-6 py-4 font-semibold">Selection</th>
              <th className="px-6 py-4 text-right font-semibold">Odds</th>
              <th className="px-6 py-4 text-right font-semibold">True Prob</th>
              <th className="px-6 py-4 text-right font-semibold">Edge</th>
              <th className="px-6 py-4 text-center font-semibold">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700 bg-slate-900">
            {bets.map((bet, index) => {
              const id = `${bet.match_id}-${bet.bookmaker}-${bet.outcome}-${index}`;
              const isExpanded = expandedBetId === id;
              const edgeBadge = getEdgeBadge(bet.edge);

              return (
                <Fragment key={id}>
                  <tr
                    className={`hover:bg-slate-800/50 cursor-pointer transition-colors ${isExpanded ? 'bg-slate-800/50' : ''}`}
                    onClick={() => toggleExpand(id)}
                  >
                    <td className="px-6 py-4 font-medium text-slate-100">
                      <div className="font-semibold">{bet.home_team} vs {bet.away_team}</div>
                    </td>
                    <td className="px-6 py-4 text-slate-400">
                      {new Date(bet.commence_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-slate-800 rounded text-xs font-medium text-slate-300">
                        {bet.bookmaker}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-emerald-400 font-semibold">
                      {bet.outcome}
                    </td>
                    <td className="px-6 py-4 text-right font-bold text-slate-100 text-base">
                      {bet.odds.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-right text-slate-300">
                      {(bet.true_probability * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <span className={`font-bold text-lg ${getEdgeColor(bet.edge)}`}>
                          +{bet.edge.toFixed(1)}%
                        </span>
                        <span className={`px-2 py-0.5 text-xs rounded border ${edgeBadge.color}`}>
                          {edgeBadge.text}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <div className="flex gap-2 justify-center">
                        <a
                          href={bet.affiliate_url || "#"}
                          target="_blank"
                          rel="noopener noreferrer"
                          onClick={(e) => e.stopPropagation()}
                          className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-md text-xs font-bold transition-all hover:scale-105 hover:shadow-lg hover:shadow-emerald-500/50 flex items-center gap-1"
                        >
                          BET NOW
                          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                          </svg>
                        </a>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            placeBet(bet);
                          }}
                          className="bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-2 rounded-md text-xs font-medium transition-colors"
                          title="Track as Paper Bet"
                        >
                          Track
                        </button>
                      </div>
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr className="bg-slate-800/30 border-t border-slate-700/50">
                      <td colSpan={8} className="p-6">
                        <div className="flex gap-6">
                          <div className="w-1/3">
                            <RadarVisualizer bet={bet} />
                          </div>
                          <div className="w-2/3 space-y-4">
                            <div>
                              <h4 className="font-bold text-slate-100 mb-2 text-lg">Value Analysis</h4>
                              <p className="text-slate-300 leading-relaxed">
                                This bet has a <strong className={getEdgeColor(bet.edge)}>+{bet.edge.toFixed(1)}% edge</strong> against the market.
                                The true probability is estimated at <strong>{(bet.true_probability * 100).toFixed(1)}%</strong> based on sharp bookmaker consensus.
                              </p>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                              <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
                                <div className="text-xs text-slate-500 mb-1">Expected Value</div>
                                <div className="font-mono text-2xl text-emerald-400">+{bet.expected_value}%</div>
                              </div>
                              <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
                                <div className="text-xs text-slate-500 mb-1">Recommended Stake</div>
                                <div className="font-mono text-2xl text-blue-400">$100</div>
                                <div className="text-xs text-slate-500 mt-1">Flat betting strategy</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
