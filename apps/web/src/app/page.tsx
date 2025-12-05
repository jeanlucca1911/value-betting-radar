"use client";

import { useState } from 'react';
import { useLiveOdds } from '@/hooks/useLiveOdds';
import { OddsTable } from "@/components/OddsTable";
import { LeagueSelector } from '@/components/LeagueSelector';
import { LoadingSkeleton } from '@/components/LoadingStates';
import { EmptyState } from "@/components/EmptyState";
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { ArrowRight, TrendingUp, ShieldCheck, Zap, Radar } from 'lucide-react';
import Link from 'next/link';
import { EnhancedStatCard } from '@/components/AnimatedStats';
import { TestimonialsCarousel } from '@/components/TestimonialsCarousel';
import { ComparisonTable } from '@/components/ComparisonTable';

import { usePortfolioStats } from '@/hooks/usePortfolioStats';

export default function Dashboard() {
  const [sport, setSport] = useState("soccer_epl");
  const { data, error, isLoading } = useLiveOdds(sport, "us"); // Use "us" region by default
  const { stats } = usePortfolioStats();

  // Calculate average edge from live data if available
  const avgEdge = data && data.length > 0
    ? (data.reduce((acc, bet) => acc + bet.edge, 0) / data.length).toFixed(1)
    : "0.0";

  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section */}
      <section className="relative -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 py-20 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-slate-950">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[400px] bg-emerald-500/20 blur-[100px] rounded-full opacity-50" />
        </div>

        <div className="relative max-w-5xl mx-auto text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 backdrop-blur-sm"
          >
            <Badge variant="success" className="animate-pulse">LIVE</Badge>
            <span className="text-sm text-slate-300">System Active • Scanning 42 Bookmakers</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold tracking-tight text-white"
          >
            Discover Value. <br />
            <span className="bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent">
              Beat the Odds.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed"
          >
            Our advanced algorithms scan thousands of markets in real-time to find
            mispriced odds, giving you a mathematical edge over the bookmakers.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link href="/advanced">
              <Button size="lg" variant="premium" className="group text-base h-12 px-8">
                Start Hunting Value
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link href="/portfolio">
              <Button size="lg" variant="outline" className="text-base h-12 px-8">
                View Portfolio
              </Button>
            </Link>
          </motion.div>

          {/* Trust Signals */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="pt-8 flex items-center justify-center gap-8 text-slate-500 text-sm"
          >
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4" />
              <span>Verified Data</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="h-4 w-4" />
              <span>Real-time Updates</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              <span>+15% Avg. ROI</span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Overview with Premium Components */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <EnhancedStatCard
          title="Total Profit"
          value={stats ? Math.abs(stats.net_profit) : 0}
          valuePrefix="$"
          change={12}
          sparklineData={[100, 120, 115, 140, 160, 155, 180]}
          icon={<TrendingUp className="h-6 w-6" />}
          iconColor="emerald"
        />
        <EnhancedStatCard
          title="Active Opportunities"
          value={data ? data.length : 0}
          change={8}
          sparklineData={[5, 8, 6, 12, 10, 15, data?.length || 0]}
          icon={<Zap className="h-6 w-6" />}
          iconColor="blue"
        />
        <EnhancedStatCard
          title="Average Edge"
          value={avgEdge}
          valueSuffix="%"
          change={5}
          sparklineData={[3.2, 3.5, 4.1, 3.8, 4.5, 4.2, parseFloat(avgEdge)]}
          icon={<Radar className="h-6 w-6" />}
          iconColor="purple"
        />
      </div>

      {/* Live Opportunities Table */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
              Live Opportunities
            </h2>
            <p className="text-slate-400">Real-time value bets from 42+ bookmakers</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => window.location.reload()}>
            Refresh Data
          </Button>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <LeagueSelector currentLeague={sport} onLeagueSelect={setSport} />
        </div>

        {error ? (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center">
            <p className="text-red-400">Unable to load live odds. Please try again later.</p>
            <Button variant="outline" className="mt-4 border-red-500/30 hover:bg-red-500/10" onClick={() => window.location.reload()}>
              Retry Connection
            </Button>
          </div>
        ) : isLoading ? (
          <LoadingSkeleton />
        ) : data && data.length > 0 ? (
          <OddsTable bets={data} />
        ) : (
          <EmptyState sport={sport} />
        )}
      </div>

      {/* Testimonials Section */}
      <section className="py-16">
        <TestimonialsCarousel />
      </section>

      {/* Comparison Table */}
      <section className="py-16">
        <ComparisonTable />
      </section>

      {/* Final CTA */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center py-20 bg-gradient-to-br from-emerald-500/10 to-teal-500/10 rounded-3xl border border-emerald-500/20"
      >
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
          Ready to Start Winning?
        </h2>
        <p className="text-slate-400 text-lg mb-8 max-w-2xl mx-auto">
          Join thousands of data-driven bettors who've discovered the power of Bayesian probability
        </p>
        <Link href="/register">
          <Button size="lg" variant="premium" className="group text-lg h-14 px-10">
            Get Started Free
            <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </Link>
      </motion.section>
    </div>
  );
}
