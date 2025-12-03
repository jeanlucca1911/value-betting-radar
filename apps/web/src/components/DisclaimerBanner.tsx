"use client";

export default function DisclaimerBanner() {
    return (
        <div className="bg-yellow-500/10 border-y border-yellow-500/20 py-3 px-4">
            <div className="max-w-7xl mx-auto">
                <p className="text-sm text-yellow-200 text-center">
                    <strong>⚠️ Disclaimer:</strong> 18+ only. Gambling can be addictive. This is not financial advice.
                    Please gamble responsibly. If you have a gambling problem, call{" "}
                    <a
                        href="tel:1-800-522-4700"
                        className="underline hover:text-yellow-100"
                    >
                        1-800-522-4700
                    </a>
                    {" "}or visit{" "}
                    <a
                        href="https://www.ncpgambling.org"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline hover:text-yellow-100"
                    >
                        ncpgambling.org
                    </a>
                </p>
            </div>
        </div>
    );
}
