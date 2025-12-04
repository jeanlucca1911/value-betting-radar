"use client";

import { motion } from "framer-motion";

interface DataFreshnessIndicatorProps {
    lastUpdated: Date;
    nextRefresh?: Date;
}

export function DataFreshnessIndicator({ lastUpdated, nextRefresh }: DataFreshnessIndicatorProps) {
    const getTimeAgo = (date: Date) => {
        const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);

        if (seconds < 60) return `${seconds}s ago`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
        return `${Math.floor(seconds / 86400)}d ago`;
    };

    const getNextRefreshTime = () => {
        if (!nextRefresh) return null;

        const seconds = Math.floor((nextRefresh.getTime() - new Date().getTime()) / 1000);
        if (seconds < 0) return "Updating...";
        if (seconds < 60) return `in ${seconds}s`;
        return `in ${Math.floor(seconds / 60)}m`;
    };

    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4 text-xs text-gray-400"
        >
            <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                <span>
                    Last updated: <strong className="text-gray-300">{getTimeAgo(lastUpdated)}</strong>
                </span>
            </div>
            {nextRefresh && (
                <>
                    <div className="w-px h-4 bg-gray-700" />
                    <span>
                        Next refresh: <strong className="text-gray-300">{getNextRefreshTime()}</strong>
                    </span>
                </>
            )}
            <div className="ml-auto flex items-center gap-1">
                <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                <span className="text-emerald-400 font-medium">LIVE DATA</span>
            </div>
        </motion.div>
    );
}
