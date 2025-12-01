export function LoadingSkeleton() {
    return (
        <div className="animate-pulse">
            <div className="overflow-x-auto rounded-lg border border-slate-700">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-800 text-xs uppercase text-slate-400">
                        <tr>
                            <th className="px-6 py-3">Match</th>
                            <th className="px-6 py-3">Time</th>
                            <th className="px-6 py-3">Bookmaker</th>
                            <th className="px-6 py-3">Bet</th>
                            <th className="px-6 py-3 text-right">Odds</th>
                            <th className="px-6 py-3 text-right">Probability</th>
                            <th className="px-6 py-3 text-right">Edge</th>
                            <th className="px-6 py-3 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700 bg-slate-900">
                        {[...Array(5)].map((_, i) => (
                            <tr key={i}>
                                <td className="px-6 py-4">
                                    <div className="h-4 bg-slate-700 rounded w-32"></div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="h-4 bg-slate-700 rounded w-16"></div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="h-4 bg-slate-700 rounded w-20"></div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="h-4 bg-slate-700 rounded w-24"></div>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="h-4 bg-slate-700 rounded w-12 ml-auto"></div>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="h-4 bg-slate-700 rounded w-16 ml-auto"></div>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="h-4 bg-slate-700 rounded w-12 ml-auto"></div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <div className="h-8 bg-slate-700 rounded w-16 mx-auto"></div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export function EmptyState() {
    return (
        <div className="text-center p-12 bg-slate-800 rounded-lg border border-slate-700">
            <svg className="mx-auto h-12 w-12 text-slate-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-lg font-semibold text-slate-200 mb-2">No Value Bets Right Now</h3>
            <p className="text-slate-400 max-w-md mx-auto">
                We&apos;re continuously scanning the markets. Value opportunities appear when bookmakers misprice odds. Check back soon!
            </p>
            <div className="mt-6 flex items-center justify-center gap-2 text-sm text-slate-500">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span>Live scanning active</span>
            </div>
        </div>
    );
}
