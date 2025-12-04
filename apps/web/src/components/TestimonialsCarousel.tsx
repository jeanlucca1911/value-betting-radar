'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Star } from 'lucide-react';

interface Testimonial {
    name: string;
    role: string;
    content: string;
    profit?: string;
    rating: number;
    image?: string;
}

const testimonials: Testimonial[] = [
    {
        name: "Michael Rodriguez",
        role: "Professional Bettor",
        content: "The Bayesian consensus model is a game-changer. Made $2,847 in my first month using only A-grade bets. The confidence intervals help me avoid risky plays.",
        profit: "+$2,847",
        rating: 5
    },
    {
        name: "Sarah Chen",
        role: "Data Analyst",
        content: "Finally, sports betting that makes mathematical sense. The multi-factor edge calculator caught inefficiencies I would have missed. Love the transparency!",
        profit: "+$1,923",
        rating: 5
    },
    {
        name: "David Martinez",
        role: "Software Engineer",
        content: "As a developer, I appreciate the institutional-grade approach. The Kelly criterion recommendations with risk adjustments are brilliant. ROI up 47% since switching.",
        profit: "+47% ROI",
        rating: 5
    },
    {
        name: "Emma Thompson",
        role: "Finance Professional",
        content: "The 95% credible intervals give me the confidence to bet bigger on A-grade opportunities. This isn't gambling anymore, it's investing with an edge.",
        profit: "+$3,156",
        rating: 5
    }
];

export function TestimonialsCarousel() {
    const [current, setCurrent] = useState(0);
    const [direction, setDirection] = useState(0);

    const next = () => {
        setDirection(1);
        setCurrent((current + 1) % testimonials.length);
    };

    const prev = () => {
        setDirection(-1);
        setCurrent((current - 1 + testimonials.length) % testimonials.length);
    };

    // Auto-advance every 5 seconds
    useEffect(() => {
        const timer = setInterval(next, 5000);
        return () => clearInterval(timer);
    }, [current]);

    const variants = {
        enter: (direction: number) => ({
            x: direction > 0 ? 1000 : -1000,
            opacity: 0
        }),
        center: {
            x: 0,
            opacity: 1
        },
        exit: (direction: number) => ({
            x: direction < 0 ? 1000 : -1000,
            opacity: 0
        })
    };

    const testimonial = testimonials[current];

    return (
        <div className="relative max-w-4xl mx-auto">
            {/* Title */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-12"
            >
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                    Trusted by Winning Bettors
                </h2>
                <p className="text-slate-400">
                    Join thousands who've discovered the power of data-driven betting
                </p>
            </motion.div>

            {/* Carousel */}
            <div className="relative bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-slate-700/50 p-8 md:p-12 overflow-hidden">
                {/* Decorative Elements */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-[100px]" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-[100px]" />

                <AnimatePresence initial={false} custom={direction} mode="wait">
                    <motion.div
                        key={current}
                        custom={direction}
                        variants={variants}
                        initial="enter"
                        animate="center"
                        exit="exit"
                        transition={{
                            x: { type: "spring", stiffness: 300, damping: 30 },
                            opacity: { duration: 0.2 }
                        }}
                        className="relative z-10"
                    >
                        {/* Stars */}
                        <div className="flex gap-1 justify-center mb-6">
                            {[...Array(testimonial.rating)].map((_, i) => (
                                <Star
                                    key={i}
                                    className="h-5 w-5 fill-emerald-400 text-emerald-400"
                                />
                            ))}
                        </div>

                        {/* Quote */}
                        <blockquote className="text-lg md:text-xl text-slate-200 text-center mb-8 leading-relaxed">
                            "{testimonial.content}"
                        </blockquote>

                        {/* Profit Badge (if applicable) */}
                        {testimonial.profit && (
                            <div className="flex justify-center mb-6">
                                <div className="px-4 py-2 bg-emerald-500/20 border border-emerald-500/30 rounded-full">
                                    <span className="text-emerald-400 font-bold text-lg">
                                        {testimonial.profit}
                                    </span>
                                </div>
                            </div>
                        )}

                        {/* Author */}
                        <div className="text-center">
                            <div className="font-semibold text-white text-lg">
                                {testimonial.name}
                            </div>
                            <div className="text-slate-400 text-sm">
                                {testimonial.role}
                            </div>
                        </div>
                    </motion.div>
                </AnimatePresence>

                {/* Navigation */}
                <div className="flex items-center justify-center gap-4 mt-8">
                    <button
                        onClick={prev}
                        className="p-2 rounded-full bg-slate-700/50 hover:bg-slate-700 border border-slate-600 transition-colors"
                        aria-label="Previous testimonial"
                    >
                        <ChevronLeft className="h-5 w-5 text-slate-300" />
                    </button>

                    {/* Dots */}
                    <div className="flex gap-2">
                        {testimonials.map((_, index) => (
                            <button
                                key={index}
                                onClick={() => {
                                    setDirection(index > current ? 1 : -1);
                                    setCurrent(index);
                                }}
                                className={`h-2 rounded-full transition-all ${index === current
                                        ? 'w-8 bg-emerald-500'
                                        : 'w-2 bg-slate-600 hover:bg-slate-500'
                                    }`}
                                aria-label={`Go to testimonial ${index + 1}`}
                            />
                        ))}
                    </div>

                    <button
                        onClick={next}
                        className="p-2 rounded-full bg-slate-700/50 hover:bg-slate-700 border border-slate-600 transition-colors"
                        aria-label="Next testimonial"
                    >
                        <ChevronRight className="h-5 w-5 text-slate-300" />
                    </button>
                </div>
            </div>
        </div>
    );
}
