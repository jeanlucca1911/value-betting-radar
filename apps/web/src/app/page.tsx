```javascript
"use client";

import { useState} from 'react';
import { useLiveOdds} from '@/hooks/useLiveOdds';
import { ValueBetCard} from "@/components/ValueBetCard";
import { LeagueSelector} from '@/components/LeagueSelector';
import { LoadingSkeleton} from '@/components/LoadingStates';
import { EmptyState} from "@/components/EmptyState";
import { motion} from 'framer-motion';
import { Button} from '@/components/ui/Button';
import { Badge} from '@/components/ui/Badge';
import { ArrowRight, TrendingUp, ShieldCheck, Zap, Radar} from 'lucide-react';
import Link from 'next/link';

import { usePortfolioStats} from '@/hooks/usePortfolioStats';

export default function Dashboard() {
  const [sport, setSport] = useState("soccer_epl");
  const { data, error, isLoading} = useLiveOdds(sport, "us"); // Use "us" region by default
  const { stats} = usePortfolioStats();

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
            initial={{ opacity: 0, y: 20}}
            animate={{ opacity: 1, y: 0}}
            transition={{ duration: 0.5}}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 backdrop-blur-sm"
          >
            <Badge variant="success" className="animate-pulse">LIVE</Badge>
            <span className="text-sm text-slate-300">System Active • Scanning 42 Bookmakers</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20}}
            animate={{ opacity: 1, y: 0}}
            transition={{ duration: 0.5, delay: 0.1}}
            className="text-5xl md:text-7xl font-bold tracking-tight text-white"
          >
            Discover Value. <br />
            <span className="bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent">
              Beat the Odds.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20}}
            animate={{ opacity: 1, y: 0}}
            transition={{ duration: 0.5, delay: 0.2}}
            className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed"
          >
            Our advanced algorithms scan thousands of markets in real-time to find
            mispriced odds, giving you a mathematical edge over the bookmakers.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20}}
            animate={{ opacity: 1, y: 0}}
            transition={{ duration: 0.5, delay: 0.3}}
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
            initial={{ opacity: 0}}
            animate={{ opacity: 1}}
            transition={{ duration: 0.5, delay: 0.5}}
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

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800/50 backdrop-blur p-6 rounded-2xl border border-slate-700/50">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-2 bg-emerald-500/10 rounded-lg">
              <TrendingUp className="h-6 w-6 text-emerald-400" />
            </div>
            <h3 className="text-slate-400 font-medium">Total Profit</h3>
          </div>
          <p className={'text-3xl font-bold ' + (stats && stats.net_profit >= 0 ? 'text-emerald-400' : 'text-red-400')}>
            {stats ? `$${ Math.abs(stats.net_profit).toFixed(2) } ` : '$0.00'}
          </p>
          <p className="text-sm text-slate-500 mt-1">
            {stats ? `${ stats.net_profit >= 0 ? '+' : '' }${ stats.net_profit.toFixed(2) } all time` : 'Start betting to see stats'}
          </p>
        </div>
        <div className="bg-slate-800/50 backdrop-blur p-6 rounded-2xl border border-slate-700/50">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Zap className="h-6 w-6 text-blue-400" />
            </div>
            <h3 className="text-slate-400 font-medium">Active Opportunities</h3>
          </div>
          <p className="text-3xl font-bold text-white">{data ? data.length : 0}</p>
          <p className="text-sm text-slate-500 mt-1">Updated just now</p>
        </div>
        <div className="bg-slate-800/50 backdrop-blur p-6 rounded-2xl border border-slate-700/50">
          <div className="flex items-center gap-4 mb-2">
            <div className="p-2 bg-purple-500/10 rounded-lg">
              <Radar className="h-6 w-6 text-purple-400" />
            </div>
            <h3 className="text-slate-400 font-medium">Avg. Edge</h3>
          </div>
          <p className="text-3xl font-bold text-white">{avgEdge}%</p>
          <p className="text-sm text-purple-400 mt-1">High value detected</p>
        </div>
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
    </div>
  );
}
