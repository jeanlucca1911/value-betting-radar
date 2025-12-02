"use client";

export default function TermsPage() {
    return (
        <div className="min-h-screen bg-slate-950 py-12 px-4">
            <div className="max-w-4xl mx-auto bg-slate-900/50 backdrop-blur-xl p-8 rounded-2xl border border-slate-800">
                <h1 className="text-4xl font-bold text-white mb-8">Terms of Service</h1>

                <div className="prose prose-invert max-w-none space-y-6 text-slate-300">
                    <p className="text-sm text-slate-500">Last updated: December 2, 2024</p>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">1. Acceptance of Terms</h2>
                        <p>
                            By accessing and using Value Betting Radar, you accept and agree to be bound by the terms and
                            provision of this agreement. If you do not agree to these terms, please do not use this service.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">2. Description of Service</h2>
                        <p>
                            Value Betting Radar is an educational tool that provides sports betting analytics, odds comparison,
                            and value bet identification. We use mathematical models to calculate theoretical "true probabilities"
                            and identify potential value in betting markets.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">3. Not Financial Advice</h2>
                        <div className="bg-yellow-500/10 border border-yellow-500/20 p-4 rounded-lg">
                            <p className="font-semibold text-yellow-400">Disclaimer:</p>
                            <p className="mt-2">
                                Value Betting Radar is for informational and educational purposes only. We do not provide
                                financial, investment, or gambling advice. All betting decisions are made at your own risk.
                                Past performance does not guarantee future results.
                            </p>
                        </div>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">4. User Responsibilities</h2>
                        <p>You agree to:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Be at least 18 years old (or 21+ where required by law)</li>
                            <li>Comply with all local laws regarding sports betting</li>
                            <li>Use the service for personal, non-commercial purposes only</li>
                            <li>Not attempt to reverse-engineer or scrape our algorithms</li>
                            <li>Not share your account credentials with others</li>
                            <li>Gamble responsibly and within your means</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">5. Paper Trading Only</h2>
                        <p>
                            Our portfolio tracking feature is for "paper trading" (simulated betting) only. We do not handle
                            real money, process payments, or place actual bets on your behalf. All betting must be done
                            directly with licensed bookmakers.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">6. Affiliate Relationships</h2>
                        <p>
                            We participate in affiliate programs with various bookmakers. When you click on a bookmaker link
                            and create an account, we may receive a commission. This relationship does not influence our
                            mathematical calculations or value bet identification, which are purely algorithmic.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">7. Accuracy and Reliability</h2>
                        <p>
                            While we strive for accuracy, we cannot guarantee that all odds data is 100% accurate or up-to-date.
                            Odds can change rapidly. Always verify odds directly with the bookmaker before placing any bet.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">8. Limitation of Liability</h2>
                        <p>
                            Value Betting Radar and its operators shall not be liable for any losses, damages, or claims
                            arising from:
                        </p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Use or inability to use the service</li>
                            <li>Betting losses based on our recommendations</li>
                            <li>Inaccurate or outdated odds data</li>
                            <li>Service interruptions or downtime</li>
                            <li>Third-party bookmaker actions or policies</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">9. Responsible Gambling</h2>
                        <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-lg">
                            <p className="font-semibold text-red-400">Gambling Addiction Warning:</p>
                            <p className="mt-2">
                                Gambling can be addictive. If you or someone you know has a gambling problem, please seek help:
                            </p>
                            <ul className="list-disc pl-6 mt-2 space-y-1">
                                <li>National Council on Problem Gambling: 1-800-522-4700</li>
                                <li>GamCare (UK): 0808 8020 133</li>
                                <li>Gambling Therapy: <a href="https://www.gamblingtherapy.org" className="text-purple-400">gamblingtherapy.org</a></li>
                            </ul>
                        </div>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">10. Account Termination</h2>
                        <p>
                            We reserve the right to suspend or terminate your account at any time for violation of these terms,
                            fraudulent activity, or any other reason we deem necessary.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">11. Intellectual Property</h2>
                        <p>
                            All content, algorithms, designs, and trademarks on Value Betting Radar are the property of the
                            service operators. You may not copy, modify, or distribute any part of the service without
                            explicit permission.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">12. Changes to Terms</h2>
                        <p>
                            We may modify these terms at any time. Continued use of the service after changes constitutes
                            acceptance of the new terms.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">13. Governing Law</h2>
                        <p>
                            These terms shall be governed by and construed in accordance with applicable laws. Any disputes
                            shall be resolved in the appropriate courts.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">14. Contact</h2>
                        <p>
                            For questions about these Terms of Service, contact us at:{" "}
                            <a href="mailto:legal@valuebettingradar.com" className="text-purple-400 hover:text-purple-300">
                                legal@valuebettingradar.com
                            </a>
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
}
