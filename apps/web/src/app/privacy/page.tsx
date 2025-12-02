"use client";

export default function PrivacyPage() {
    return (
        <div className="min-h-screen bg-slate-950 py-12 px-4">
            <div className="max-w-4xl mx-auto bg-slate-900/50 backdrop-blur-xl p-8 rounded-2xl border border-slate-800">
                <h1 className="text-4xl font-bold text-white mb-8">Privacy Policy</h1>

                <div className="prose prose-invert max-w-none space-y-6 text-slate-300">
                    <p className="text-sm text-slate-500">Last updated: December 2, 2024</p>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">1. Information We Collect</h2>
                        <p>We collect information you provide directly to us when you:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Create an account (email address)</li>
                            <li>Track bets in your portfolio</li>
                            <li>Use our parlay builder and other tools</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">2. How We Use Your Information</h2>
                        <p>We use the information we collect to:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Provide, maintain, and improve our services</li>
                            <li>Send you technical notices and support messages</li>
                            <li>Track your betting performance (paper trading only)</li>
                            <li>Analyze usage patterns to improve our algorithms</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">3. Affiliate Disclosure</h2>
                        <div className="bg-purple-500/10 border border-purple-500/20 p-4 rounded-lg">
                            <p className="font-semibold text-purple-400">Important Notice:</p>
                            <p className="mt-2">
                                Value Betting Radar participates in affiliate marketing programs. When you click on bookmaker links
                                and create an account, we may earn a commission. This does not affect the price you pay or the
                                quality of our recommendations. We only recommend bookmakers we believe offer fair odds and reliable service.
                            </p>
                        </div>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">4. Cookies and Tracking</h2>
                        <p>We use cookies and similar tracking technologies to:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Keep you logged in</li>
                            <li>Remember your preferences (selected leagues, regions)</li>
                            <li>Analyze site traffic and usage patterns</li>
                            <li>Track affiliate link clicks (for commission purposes)</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">5. Data Security</h2>
                        <p>
                            We implement appropriate security measures to protect your personal information. Your password is
                            hashed using industry-standard bcrypt encryption. We never store your password in plain text.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">6. Third-Party Services</h2>
                        <p>We use the following third-party services:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li><strong>The Odds API</strong>: For real-time sports betting odds</li>
                            <li><strong>Vercel</strong>: For hosting our frontend</li>
                            <li><strong>Railway</strong>: For hosting our backend</li>
                            <li><strong>Affiliate Networks</strong>: For bookmaker referrals</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">7. Your Rights</h2>
                        <p>You have the right to:</p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>Access your personal data</li>
                            <li>Request deletion of your account and data</li>
                            <li>Opt-out of marketing communications</li>
                            <li>Export your betting history</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">8. Age Restriction</h2>
                        <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-lg">
                            <p className="font-semibold text-red-400">18+ Only:</p>
                            <p className="mt-2">
                                You must be at least 18 years old (or 21+ in some jurisdictions) to use this service.
                                Sports betting may be illegal in your jurisdiction. It is your responsibility to ensure
                                compliance with local laws.
                            </p>
                        </div>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">9. Changes to This Policy</h2>
                        <p>
                            We may update this privacy policy from time to time. We will notify you of any changes by
                            posting the new policy on this page and updating the "Last updated" date.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-white mt-8 mb-4">10. Contact Us</h2>
                        <p>
                            If you have any questions about this Privacy Policy, please contact us at:{" "}
                            <a href="mailto:privacy@valuebettingradar.com" className="text-purple-400 hover:text-purple-300">
                                privacy@valuebettingradar.com
                            </a>
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
}
