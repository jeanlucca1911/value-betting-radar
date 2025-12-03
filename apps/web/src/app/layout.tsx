import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { NavBar } from "@/components/NavBar";
import { ParlayProvider } from "@/context/ParlayContext";
import { ParlaySlip } from "@/components/ParlaySlip";
import { Footer } from "@/components/Footer";
import { DisclaimerBanner } from "@/components/DisclaimerBanner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Value Betting Radar",
  description: "Detect and exploit market inefficiencies in soccer betting.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ParlayProvider>
          <NavBar />
          <DisclaimerBanner />
          <main className="max-w-7xl mx-auto p-8">{children}</main>
          <ParlaySlip />
          <Footer />
        </ParlayProvider>
      </body>
    </html>
  );
}
