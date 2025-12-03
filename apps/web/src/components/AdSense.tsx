"use client";

import Script from 'next/script';

export default function AdSense() {
    return (
        <>
            <Script
                async
                src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
                crossOrigin="anonymous"
                strategy="afterInteractive"
            />
        </>
    );
}

// Display Ad Component (300x250)
export function DisplayAd() {
    return (
        <div className="my-4 flex justify-center">
            <ins
                className="adsbygoogle"
                style={{ display: 'block' }}
                data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                data-ad-slot="XXXXXXXXXX"
                data-ad-format="auto"
                data-full-width-responsive="true"
            />
        </div>
    );
}

// Sidebar Ad Component (160x600)
export function SidebarAd() {
    return (
        <div className="sticky top-4">
            <ins
                className="adsbygoogle"
                style={{ display: 'block' }}
                data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                data-ad-slot="XXXXXXXXXX"
                data-ad-format="auto"
                data-full-width-responsive="true"
            />
        </div>
    );
}
