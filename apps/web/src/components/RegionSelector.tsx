"use client";

import { cn } from "@/lib/utils";

interface RegionSelectorProps {
    selectedRegion: string;
    onSelect: (region: string) => void;
}

const REGIONS = [
    { id: "uk", name: "UK", flag: "🇬🇧" },
    { id: "eu", name: "Europe", flag: "🇪🇺" },
    { id: "us", name: "USA", flag: "🇺🇸" },
    { id: "au", name: "Australia", flag: "🇦🇺" },
];

export function RegionSelector({ selectedRegion, onSelect }: RegionSelectorProps) {
    return (
        <div className="flex items-center gap-2 bg-slate-800/50 p-1 rounded-lg border border-slate-700 w-fit">
            {REGIONS.map((region) => (
                <button
                    key={region.id}
                    onClick={() => onSelect(region.id)}
                    className={cn(
                        "px-3 py-1.5 rounded-md text-xs font-medium transition-all flex items-center gap-1.5",
                        selectedRegion === region.id
                            ? "bg-slate-700 text-white shadow-sm"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-700/50"
                    )}
                >
                    <span>{region.flag}</span>
                    {region.name}
                </button>
            ))}
        </div>
    );
}
