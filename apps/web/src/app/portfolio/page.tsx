"use client";

import { PortfolioDashboard } from '@/components/PortfolioDashboard';

export default function PortfolioPage() {
    return (
        <div className="space-y-8">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-slate-100 mb-4">
                    My <span className="text-emerald-400">Portfolio</span>
                </h1>
                <p className="text-slate-400 text-lg">
                    Track your betting performance, ROI, and profit over time.
                </p>
            </div>

            <PortfolioDashboard />
        </div>
    );
}
