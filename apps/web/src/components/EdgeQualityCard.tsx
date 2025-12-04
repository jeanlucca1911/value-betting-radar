'use client';

import { motion } from 'framer-motion';
import { Target, TrendingUp, Shield } from 'lucide-react';

interface EdgeQualityProps {
    rawEdge: number;  // Raw mathematical edge
    riskAdjustedEdge: number;  // After multi-factor penalties
    qualityScore: number;  // 0-100
    components?: {
        uncertainty: number;
        liquidity: number;
        reliability: number;
        clv: number;
    };
}

export function EdgeQualityCard({
    rawEdge,
    riskAdjustedEdge,
    qualityScore,
    components
}: EdgeQualityProps) {
    const getQualityGrade = (score: number): { grade: string; color: string; glow: boolean } => {
        if (score >= 80) return { grade: 'Premium', color: 'emerald', glow: true };
        if (score >= 60) return { grade: 'Good', color: 'blue', glow: false };
        if (score >= 40) return { grade: 'Fair', color: 'yellow', glow: false };
        return { grade: 'Poor', color: 'gray', glow: false };
    };

    const quality = getQualityGrade(qualityScore);

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`relative rounded-xl border-2 border-${quality.color}-500/30 bg-gradient-to-br from-slate-800/80 to-slate-900/80 p-5 backdrop-blur-sm ${quality.glow ? 'shadow-2xl shadow-emerald-500/20' : ''}`}
        >
            {/* Quality Badge */}
            <div className="flex items-center justify-between mb-4">
                <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-${quality.color}-500/20 border border-${quality.color}-500/40`}>
                    <Shield className={`h-4 w-4 text-${quality.color}-400`} />
                    <span className={`text-sm font-bold text-${quality.color}-400`}>
                        {quality.grade} Quality
                    </span>
                </div>

                <div className="text-right">
                    <div className="text-2xl font-bold text-white">
                        {(riskAdjustedEdge * 100).toFixed(2)}%
                    </div>
                    <div className="text-xs text-slate-400">
                        Risk-Adjusted Edge
                    </div>
                </div>
            </div>

            {/* Quality Score Bar */}
            <div className="relative h-2 bg-slate-700/50 rounded-full overflow-hidden mb-3">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${qualityScore}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                    className={`h-full bg-gradient-to-r from-${quality.color}-500 to-${quality.color}-400`}
                />
            </div>

            {/* Edge Comparison */}
            <div className="grid grid-cols-2 gap-3 mb-3">
                <div className="bg-slate-800/50 rounded-lg p-2.5">
                    <div className="flex items-center gap-1.5 mb-1">
                        <Target className="h-3.5 w-3.5 text-slate-400" />
                        <span className="text-xs text-slate-400">Raw Edge</span>
                    </div>
                    <div className="text-lg font-bold text-slate-300">
                        +{(rawEdge * 100).toFixed(2)}%
                    </div>
                </div>

                <div className="bg-slate-800/50 rounded-lg p-2.5">
                    <div className="flex items-center gap-1.5 mb-1">
                        <TrendingUp className="h-3.5 w-3.5 text-emerald-400" />
                        <span className="text-xs text-slate-400">Adjusted</span>
                    </div>
                    <div className={`text-lg font-bold text-${quality.color}-400`}>
                        +{(riskAdjustedEdge * 100).toFixed(2)}%
                    </div>
                </div>
            </div>

            {/* Factor Breakdown */}
            {components && (
                <div className="space-y-1.5">
                    <div className="text-xs font-semibold text-slate-400 mb-2">
                        Risk Factors
                    </div>
                    {[
                        { name: 'Uncertainty', value: components.uncertainty, icon: '📊' },
                        { name: 'Liquidity', value: components.liquidity, icon: '💧' },
                        { name: 'Reliability', value: components.reliability, icon: '🎯' },
                        { name: 'CLV', value: components.clv, icon: '📈' }
                    ].map((factor) => (
                        <div key={factor.name} className="flex items-center justify-between text-xs">
                            <span className="text-slate-400 flex items-center gap-1.5">
                                <span>{factor.icon}</span>
                                {factor.name}
                            </span>
                            <span className={`font-semibold ${factor.value > 0.8 ? 'text-emerald-400' : factor.value > 0.5 ? 'text-blue-400' : 'text-yellow-400'}`}>
                                {(factor.value * 100).toFixed(0)}%
                            </span>
                        </div>
                    ))}
                </div>
            )}

            {/* Glow animation for premium bets */}
            {quality.glow && (
                <motion.div
                    className="absolute inset-0 rounded-xl bg-emerald-500/5"
                    animate={{
                        opacity: [0.1, 0.3, 0.1]
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: 'easeInOut'
                    }}
                />
            )}
        </motion.div>
    );
}
