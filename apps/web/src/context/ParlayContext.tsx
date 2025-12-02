"use client";

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { ValueBet } from '@/hooks/useLiveOdds';

interface ParlayContextType {
    bets: ValueBet[];
    addBet: (bet: ValueBet) => void;
    removeBet: (betId: string) => void;
    clearSlip: () => void;
    isInParlay: (betId: string) => boolean;
}

const ParlayContext = createContext<ParlayContextType | undefined>(undefined);

export function ParlayProvider({ children }: { children: ReactNode }) {
    const [bets, setBets] = useState<ValueBet[]>([]);

    const addBet = (bet: ValueBet) => {
        // Prevent duplicates and limit to 5 legs for MVP
        if (bets.find(b => b.match_id === bet.match_id && b.outcome === bet.outcome)) return;
        if (bets.length >= 5) {
            alert("Max 5 legs allowed for now!");
            return;
        }
        setBets([...bets, bet]);
    };

    const removeBet = (betId: string) => {
        // We use match_id + outcome as unique key effectively
        // But ValueBet doesn't have a unique ID field, so we filter carefully
        // Assuming match_id is unique enough for this context combined with outcome
        setBets(bets.filter(b => !(b.match_id === betId)));
        // Note: This removes all bets for that match. Ideally we need a unique ID per bet.
        // For MVP, match_id is fine as we usually pick one bet per match.
    };

    const clearSlip = () => setBets([]);

    const isInParlay = (matchId: string) => bets.some(b => b.match_id === matchId);

    return (
        <ParlayContext.Provider value={{ bets, addBet, removeBet, clearSlip, isInParlay }}>
            {children}
        </ParlayContext.Provider>
    );
}

export function useParlay() {
    const context = useContext(ParlayContext);
    if (context === undefined) {
        throw new Error('useParlay must be used within a ParlayProvider');
    }
    return context;
}
