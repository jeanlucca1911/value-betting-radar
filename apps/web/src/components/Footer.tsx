import React from 'react';
import Link from 'next/link';

export function Footer() {
    return (
        <footer className="bg-slate-900/50 backdrop-blur-xl border-t border-slate-800 mt-20">
            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Affiliate Disclosure */}
                <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-4 mb-6">
                    <p className="text-sm text-purple-300 text-center">
                        <strong>Affiliate Disclosure:</strong> We may earn a commission when you click on bookmaker links and create an account.
                        This does not affect the price you pay or our recommendations, which are based purely on mathematical analysis.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    {/* About */}
                    <div>
                        <h3 className="text-white font-bold mb-3">Value Betting Radar</h3>
                        <p className="text-slate-400 text-sm">
                            Free sports betting analytics using advanced mathematics to identify value bets.
                        </p>
                    </div>

                    {/* Legal */}
                    <div>
                        <h3 className="text-white font-bold mb-3">Legal</h3>
                        <ul className="space-y-2 text-sm">
                            <li>
                                <Link href="/privacy" className="text-slate-400 hover:text-purple-400 transition-colors">
                                    Privacy Policy
                                </Link>
                            </li>
                            <li>
                                <Link href="/terms" className="text-slate-400 hover:text-purple-400 transition-colors">
                                    Terms of Service
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Resources */}
                    <div>
                        <h3 className="text-white font-bold mb-3">Resources</h3>
                        <ul className="space-y-2 text-sm">
                            <li>
                                <a
                                    href="https://www.ncpgambling.org"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-slate-400 hover:text-purple-400 transition-colors"
                                >
                                    Problem Gambling Help
                                </a>
                            </li>
                            <li>
                                <a
                                    href="https://www.gamblingtherapy.org"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-slate-400 hover:text-purple-400 transition-colors"
                                >
                                    Gambling Therapy
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Disclaimer */}
                    <div>
                        <h3 className="text-white font-bold mb-3">Disclaimer</h3>
                        <p className="text-slate-400 text-sm">
                            18+ only. Gambling can be addictive. Please gamble responsibly. This is not financial advice.
                        </p>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="border-t border-slate-800 pt-6 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
                    <p>© 2024 Value Betting Radar. All rights reserved.</p>
                    <p className="mt-2 md:mt-0">
                        Built with ❤️ for smart bettors
                    </p>
                </div>
            </div>
        </footer>
    );
}
