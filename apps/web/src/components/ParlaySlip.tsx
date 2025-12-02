"use client";

import { useParlay } from "@/context/ParlayContext";
import { Button } from "@/components/ui/Button";
import { X, Calculator, Trash2, Ticket } from "lucide-react";
import { useState } from "react";
import { API_BASE_URL } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

export function ParlaySlip() {
    const { bets, removeBet, clearSlip } = useParlay();
    const [calculation, setCalculation] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    if (bets.length === 0) return null;

    const calculateParlay = async () => {
        setLoading(true);
        try {
            const payload = {
                bets: bets.map(b => ({
                    odds: b.odds,
                    true_probability: b.true_probability
                }))
            };

            const res = await fetch(`${API_BASE_URL}/advanced/parlay-calculator`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            setCalculation(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="fixed bottom-4 right-4 w-96 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden z-50"
        >
            {/* Header */}
            <div className="bg-slate-800 px-4 py-3 flex items-center justify-between border-b border-slate-700">
                <div className="flex items-center gap-2">
                    <Ticket className="h-5 w-5 text-emerald-400" />
                    <span className="font-bold text-white">Parlay Builder ({bets.length})</span>
                </div>
                <button onClick={clearSlip} className="text-slate-400 hover:text-red-400 transition-colors">
                    <Trash2 className="h-4 w-4" />
                </button>
            </div>

            {/* Bets List */}
            <div className="max-h-60 overflow-y-auto p-4 space-y-3">
                {bets.map((bet) => (
                    <div key={bet.match_id} className="bg-slate-800/50 p-3 rounded-lg border border-slate-700 relative group">
                        <button
                            onClick={() => removeBet(bet.match_id)}
                            className="absolute top-2 right-2 text-slate-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                            <X className="h-4 w-4" />
                        </button>
                        <div className="pr-6">
                            <div className="text-sm font-medium text-white">{bet.outcome}</div>
                            <div className="text-xs text-slate-400">{bet.home_team} vs {bet.away_team}</div>
                            <div className="flex items-center gap-2 mt-1">
                                <span className="text-emerald-400 font-bold bg-emerald-400/10 px-1.5 py-0.5 rounded text-xs">
                                    {bet.odds.toFixed(2)}
                                </span>
                                <span className="text-xs text-slate-500">{bet.bookmaker}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Calculation Result */}
            <AnimatePresence>
                {calculation && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        className="bg-emerald-900/20 border-t border-emerald-500/20 p-4 space-y-2"
                    >
                        <div className="flex justify-between text-sm">
                            <span className="text-slate-400">Combined Odds:</span>
                            <span className="text-white font-bold">{calculation.combined_odds}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-slate-400">True Probability:</span>
                            <span className="text-white font-bold">{(calculation.true_probability * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-slate-400">Total Edge:</span>
                            <span className="text-emerald-400 font-bold">+{calculation.edge_percent}%</span>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Actions */}
            <div className="p-4 bg-slate-800 border-t border-slate-700 grid grid-cols-2 gap-3">
                <Button
                    variant="outline"
                    size="sm"
                    onClick={calculateParlay}
                    disabled={loading}
                    className="w-full"
                >
                    <Calculator className="h-4 w-4 mr-2" />
                    {loading ? "..." : "Calculate"}
                </Button>
                <Button
                    variant="premium"
                    size="sm"
                    className="w-full"
                    onClick={() => alert("Parlay tracking coming soon!")}
                >
                    Place Parlay
                </Button>
            </div>
        </motion.div>
    );
}
