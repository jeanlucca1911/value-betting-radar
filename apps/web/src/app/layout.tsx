import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { NavBar } from "@/components/NavBar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Value Betting Radar",
  description: "Detect and exploit market inefficiencies in soccer betting.",
};

import { ParlayProvider } from "@/context/ParlayContext";
import { ParlaySlip } from "@/components/ParlaySlip";

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
          <main className="max-w-7xl mx-auto p-8">{children}</main>
          <ParlaySlip />
        </ParlayProvider>
      </body>
    </html>
  );
}
