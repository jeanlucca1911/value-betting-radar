'use client';

import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';

const features = [
    {
        name: 'Bayesian Consensus',
        us: true,
        competitors: false,
        tooltip: 'Hierarchical Bayesian model with 95% credible intervals'
    },
    {
        name: 'Confidence Intervals',
        us: true,
        competitors: false,
        tooltip: 'See the uncertainty range for every probability'
    },
    {
        name: 'Dynamic Kelly Sizing',
        us: true,
        competitors: false,
        tooltip: 'Adapts bet size based on quality and risk tolerance'
    },
    {
        name: 'Multi-Factor Risk Analysis',
        us: true,
        competitors: false,
        tooltip: '5-component risk adjustment system'
    },
    {
        name: 'Historical Data Training',
        us: true,
        competitors: false,
        tooltip: 'Model improves with every match tracked'
    },
    {
        name: 'Real-Time Odds',
        us: true,
        competitors: true,
        tooltip: 'Live data from 42+ bookmakers'
    },
    {
        name: 'Basic Edge Calculation',
        us: true,
        competitors: true,
        tooltip: 'Simple probability vs odds comparison'
    },
    {
        name: 'Price',
        us: 'Free',
        competitors: '$49/mo',
        tooltip: ''
    }
];

export function ComparisonTable() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto"
        >
            <div className="text-center mb-12">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                    Why We're Different
                </h2>
                <p className="text-slate-400">
                    Institutional-grade math at a fraction of the cost
                </p>
            </div>

            <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-slate-700/50 overflow-hidden">
                {/* Header */}
                <div className="grid grid-cols-3 gap-4 p-6 border-b border-slate-700/50 bg-slate-800/50">
                    <div className="text-sm font-medium text-slate-400">Feature</div>
                    <div className="text-center">
                        <div className="inline-flex px-4 py-1.5 rounded-full bg-emerald-500/20 border border-emerald-500/30">
                            <span className="text-emerald-400 font-bold">Value Betting Radar</span>
                        </div>
                    </div>
                    <div className="text-center">
                        <span className="text-slate-400 font-medium">Competitors</span>
                    </div>
                </div>

                {/* Rows */}
                {features.map((feature, index) => (
                    <motion.div
                        key={feature.name}
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.05 }}
                        className="grid grid-cols-3 gap-4 p-6 border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors group"
                    >
                        <div>
                            <div className="text-slate-200 font-medium">{feature.name}</div>
                            {feature.tooltip && (
                                <div className="text-xs text-slate-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    {feature.tooltip}
                                </div>
                            )}
                        </div>

                        <div className="flex justify-center items-center">
                            {typeof feature.us === 'boolean' ? (
                                feature.us ? (
                                    <div className="p-1.5 rounded-full bg-emerald-500/20">
                                        <Check className="h-5 w-5 text-emerald-400" />
                                    </div>
                                ) : (
                                    <div className="p-1.5 rounded-full bg-slate-700/50">
                                        <X className="h-5 w-5 text-slate-500" />
                                    </div>
                                )
                            ) : (
                                <span className="text-emerald-400 font-bold">{feature.us}</span>
                            )}
                        </div>

                        <div className="flex justify-center items-center">
                            {typeof feature.competitors === 'boolean' ? (
                                feature.competitors ? (
                                    <div className="p-1.5 rounded-full bg-blue-500/20">
                                        <Check className="h-5 w-5 text-blue-400" />
                                    </div>
                                ) : (
                                    <div className="p-1.5 rounded-full bg-slate-700/50">
                                        <X className="h-5 w-5 text-slate-500" />
                                    </div>
                                )
                            ) : (
                                <span className="text-slate-400 font-semibold">{feature.competitors}</span>
                            )}
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}
