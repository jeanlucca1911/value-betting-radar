"use client";

import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { Radar, LineChart, Zap, LogOut, LogIn, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

export function NavBar() {
    const router = useRouter();
    const pathname = usePathname();

    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [mounted, setMounted] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    // eslint-disable-next-line react-hooks/set-state-in-effect
    useEffect(() => {
        setMounted(true);
        const token = localStorage.getItem("access_token");
        setIsAuthenticated(!!token);
    }, [pathname]);

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        setIsAuthenticated(false);
        router.push("/login");
    };

    const showNav = pathname !== "/login" && pathname !== "/register";

    if (!showNav) return null;

    if (!mounted) {
        return (
            <nav className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Radar className="h-6 w-6 text-emerald-500" />
                        <span className="text-xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                            Value Betting Radar
                        </span>
                    </div>
                </div>
            </nav>
        );
    }

    const navLinks = [
        { href: "/", label: "Live Radar", icon: Zap, color: "text-emerald-400" },
        { href: "/advanced", label: "Advanced Markets", icon: Radar, color: "text-purple-400", badge: "NEW" },
        { href: "/portfolio", label: "My Portfolio", icon: LineChart, color: "text-blue-400" },
    ];

    return (
        <nav className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 transition-all duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="p-1.5 rounded-lg bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                            <Radar className="h-6 w-6 text-emerald-500" />
                        </div>
                        <span className="text-xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                            Value Betting Radar
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-1">
                        {navLinks.map((link) => {
                            const Icon = link.icon;
                            const isActive = pathname === link.href;
                            return (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    className={cn(
                                        "px-4 py-2 rounded-md text-sm font-medium transition-all flex items-center gap-2",
                                        isActive
                                            ? "bg-slate-800 text-white"
                                            : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                                    )}
                                >
                                    <Icon className={cn("h-4 w-4", isActive ? link.color : "text-slate-500")} />
                                    {link.label}
                                    {link.badge && (
                                        <span className="px-1.5 py-0.5 bg-purple-500/20 text-purple-400 text-[10px] rounded border border-purple-500/30 font-bold">
                                            {link.badge}
                                        </span>
                                    )}
                                </Link>
                            );
                        })}
                    </div>

                    {/* Auth Buttons */}
                    <div className="hidden md:flex items-center gap-4">
                        {isAuthenticated ? (
                            <Button
                                variant="destructive"
                                size="sm"
                                onClick={handleLogout}
                                className="gap-2"
                            >
                                <LogOut className="h-4 w-4" />
                                Logout
                            </Button>
                        ) : (
                            <Link href="/login">
                                <Button variant="premium" size="sm" className="gap-2">
                                    <LogIn className="h-4 w-4" />
                                    Login
                                </Button>
                            </Link>
                        )}
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <Button variant="ghost" size="icon" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
                            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </Button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {mobileMenuOpen && (
                <div className="md:hidden bg-slate-900 border-b border-slate-800">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {navLinks.map((link) => {
                            const Icon = link.icon;
                            const isActive = pathname === link.href;
                            return (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className={cn(
                                        "block px-3 py-2 rounded-md text-base font-medium flex items-center gap-3",
                                        isActive
                                            ? "bg-slate-800 text-white"
                                            : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                                    )}
                                >
                                    <Icon className={cn("h-5 w-5", isActive ? link.color : "text-slate-500")} />
                                    {link.label}
                                </Link>
                            );
                        })}
                        <div className="pt-4 pb-2 border-t border-slate-800 mt-2">
                            {isAuthenticated ? (
                                <Button
                                    variant="destructive"
                                    className="w-full justify-start gap-2"
                                    onClick={() => {
                                        handleLogout();
                                        setMobileMenuOpen(false);
                                    }}
                                >
                                    <LogOut className="h-4 w-4" />
                                    Logout
                                </Button>
                            ) : (
                                <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                                    <Button variant="premium" className="w-full justify-start gap-2">
                                        <LogIn className="h-4 w-4" />
                                        Login
                                    </Button>
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
}
