'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface AnimatedCounterProps {
    value: number;
    duration?: number;
    prefix?: string;
    suffix?: string;
    decimals?: number;
}

export function AnimatedCounter({
    value,
    duration = 2000,
    prefix = '',
    suffix = '',
    decimals = 0
}: AnimatedCounterProps) {
    const [count, setCount] = useState(0);

    useEffect(() => {
        let startTime: number;
        let animationFrame: number;

        const animate = (currentTime: number) => {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);

            // Easing function (easeOutCubic)
            const easeProgress = 1 - Math.pow(1 - progress, 3);

            setCount(value * easeProgress);

            if (progress < 1) {
                animationFrame = requestAnimationFrame(animate);
            }
        };

        animationFrame = requestAnimationFrame(animate);

        return () => cancelAnimationFrame(animationFrame);
    }, [value, duration]);

    return (
        <span>
            {prefix}
            {count.toFixed(decimals)}
            {suffix}
        </span>
    );
}

interface SparklineProps {
    data: number[];
    width?: number;
    height?: number;
    color?: string;
}

export function Sparkline({
    data,
    width = 100,
    height = 30,
    color = '#10b981'
}: SparklineProps) {
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min;

    const points = data.map((value, index) => {
        const x = (index / (data.length - 1)) * width;
        const y = height - ((value - min) / range) * height;
        return `${x},${y}`;
    }).join(' ');

    return (
        <svg width={width} height={height} className="overflow-visible">
            <motion.polyline
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 1, ease: 'easeOut' }}
                points={points}
                fill="none"
                stroke={color}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            {/* Add glow effect */}
            <motion.polyline
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 0.3 }}
                transition={{ duration: 1, ease: 'easeOut' }}
                points={points}
                fill="none"
                stroke={color}
                strokeWidth="4"
                strokeLinecap="round"
                strokeLinejoin="round"
                filter="blur(4px)"
            />
        </svg>
    );
}

interface EnhancedStatCardProps {
    title: string;
    value: string | number;
    change?: number;  // Percentage change
    sparklineData?: number[];
    icon: React.ReactNode;
    iconColor?: string;
    valuePrefix?: string;
    valueSuffix?: string;
}

export function EnhancedStatCard({
    title,
    value,
    change,
    sparklineData,
    icon,
    iconColor = 'emerald',
    valuePrefix = '',
    valueSuffix = ''
}: EnhancedStatCardProps) {
    const isPositive = change !== undefined && change >= 0;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02, y: -4 }}
            transition={{ duration: 0.2 }}
            className="group relative bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-sm p-6 rounded-2xl border border-slate-700/50 hover:border-slate-600 transition-all overflow-hidden"
        >
            {/* Background Glow */}
            <div className={`absolute inset-0 bg-${iconColor}-500/5 opacity-0 group-hover:opacity-100 transition-opacity`} />

            <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                    <div className={`p-2.5 bg-${iconColor}-500/10 rounded-xl`}>
                        <div className={`text-${iconColor}-400`}>
                            {icon}
                        </div>
                    </div>

                    {change !== undefined && (
                        <div className={`flex items-center gap-1 text-sm font-semibold ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                            <span>{isPositive ? '↑' : '↓'}</span>
                            <span>{Math.abs(change)}%</span>
                        </div>
                    )}
                </div>

                {/* Title */}
                <h3 className="text-slate-400 font-medium text-sm mb-2">
                    {title}
                </h3>

                {/* Value */}
                <div className="flex items-end justify-between mb-3">
                    <div className="text-3xl font-bold text-white">
                        {typeof value === 'number' ? (
                            <AnimatedCounter
                                value={value}
                                prefix={valuePrefix}
                                suffix={valueSuffix}
                            />
                        ) : (
                            `${valuePrefix}${value}${valueSuffix}`
                        )}
                    </div>
                </div>

                {/* Sparkline */}
                {sparklineData && (
                    <div className="mt-3 pt-3 border-t border-slate-700/50">
                        <Sparkline
                            data={sparklineData}
                            width={200}
                            height={30}
                            color={isPositive ? '#10b981' : '#ef4444'}
                        />
                    </div>
                )}
            </div>
        </motion.div>
    );
}
