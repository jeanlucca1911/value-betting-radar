'use client';

import { motion } from 'framer-motion';
import { TrendingUp, AlertCircle, CheckCircle2, Info } from 'lucide-react';

interface BayesianConfidenceProps {
    probability: number;  // 0-1
    confidenceInterval: [number, number];  // 95% CI
    confidenceScore: 'A' | 'B' | 'C' | 'D';
    effectiveSamples?: number;
    showDetails?: boolean;
}

const confidenceConfig = {
    A: {
        color: 'emerald',
        label: 'Very High',
        bgGradient: 'from-emerald-500/20 to-teal-500/20',
        borderColor: 'border-emerald-500',
        textColor: 'text-emerald-400',
        icon: CheckCircle2,
        description: 'Extremely confident in this probability'
    },
    B: {
        color: 'blue',
        label: 'High',
        bgGradient: 'from-blue-500/20 to-cyan-500/20',
        borderColor: 'border-blue-500',
        textColor: 'text-blue-400',
        icon: TrendingUp,
        description: 'Confident in this probability'
    },
    C: {
        color: 'yellow',
        label: 'Moderate',
        bgGradient: 'from-yellow-500/20 to-amber-500/20',
        borderColor: 'border-yellow-500',
        textColor: 'text-yellow-400',
        icon: Info,
        description: 'Moderate confidence - proceed with caution'
    },
    D: {
        color: 'gray',
        label: 'Low',
        bgGradient: 'from-gray-500/20 to-slate-500/20',
        borderColor: 'border-gray-500',
        textColor: 'text-gray-400',
        icon: AlertCircle,
        description: 'Low confidence - high uncertainty'
    }
};

export function BayesianConfidenceIndicator({
    probability,
    confidenceInterval,
    confidenceScore,
    effectiveSamples,
    showDetails = true
}: BayesianConfidenceProps) {
    const config = confidenceConfig[confidenceScore];
    const Icon = config.icon;

    const ciWidth = confidenceInterval[1] - confidenceInterval[0];
    const probPercent = probability * 100;
    const ciLowerPercent = confidenceInterval[0] * 100;
    const ciUpperPercent = confidenceInterval[1] * 100;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`relative overflow-hidden rounded-lg border ${config.borderColor} bg-gradient-to-br ${config.bgGradient} p-4`}
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <Icon className={`h-5 w-5 ${config.textColor}`} />
                    <span className={`text-sm font-semibold ${config.textColor}`}>
                        Grade {confidenceScore}
                    </span>
                    <span className="text-xs text-slate-400">
                        {config.label} Confidence
                    </span>
                </div>

                {effectiveSamples && (
                    <div className="text-xs text-slate-500">
                        {effectiveSamples} samples
                    </div>
                )}
            </div>

            {/* Probability Bar with CI */}
            <div className="relative h-8 bg-slate-800/50 rounded-full overflow-hidden mb-2">
                {/* CI Range (lighter background) */}
                <motion.div
                    initial={{ width: 0 }}
                    animate={{
                        width: `${ciWidth * 100}%`,
                        left: `${ciLowerPercent}%`
                    }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className={`absolute h-full bg-${config.color}-500/20`}
                    style={{ left: `${ciLowerPercent}%`, width: `${ciWidth * 100}%` }}
                />

                {/* Main Probability (darker bar) */}
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${probPercent}%` }}
                    transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
                    className={`absolute h-full bg-gradient-to-r from-${config.color}-500 to-${config.color}-400`}
                    style={{
                        boxShadow: confidenceScore === 'A'
                            ? '0 0 20px rgba(52, 211, 153, 0.5)'
                            : 'none'
                    }}
                />

                {/* Percentage Label */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-sm font-bold text-white drop-shadow-lg">
                        {probPercent.toFixed(1)}%
                    </span>
                </div>
            </div>

            {/* CI Bounds */}
            <div className="flex justify-between text-xs">
                <span className="text-slate-400">
                    {ciLowerPercent.toFixed(1)}%
                </span>
                <span className={config.textColor}>
                    95% Bayesian CI
                </span>
                <span className="text-slate-400">
                    {ciUpperPercent.toFixed(1)}%
                </span>
            </div>

            {showDetails && (
                <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    transition={{ delay: 0.5 }}
                    className="mt-3 pt-3 border-t border-slate-700/50"
                >
                    <p className="text-xs text-slate-400 italic">
                        {config.description}
                    </p>
                </motion.div>
            )}

            {/* Glow effect for A-grade bets */}
            {confidenceScore === 'A' && (
                <div className="absolute inset-0 bg-emerald-500/10 animate-pulse pointer-events-none rounded-lg" />
            )}
        </motion.div>
    );
}

// Compact version for table use
export function BayesianConfidenceBadge({
    confidenceScore,
    probability
}: Pick<BayesianConfidenceProps, 'confidenceScore' | 'probability'>) {
    const config = confidenceConfig[confidenceScore];
    const Icon = config.icon;

    return (
        <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border ${config.borderColor} bg-gradient-to-r ${config.bgGradient}`}>
            <Icon className={`h-3.5 w-3.5 ${config.textColor}`} />
            <span className={`text-xs font-semibold ${config.textColor}`}>
                {confidenceScore}
            </span>
            <span className="text-xs text-slate-400">
                {(probability * 100).toFixed(1)}%
            </span>
        </div>
    );
}
