import * as React from "react"
import { cn } from "@/lib/utils"

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning' | 'premium';
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
    const baseStyles = "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"

    const variants = {
        default: "border-transparent bg-emerald-600 text-white hover:bg-emerald-700",
        secondary: "border-transparent bg-slate-800 text-slate-100 hover:bg-slate-700",
        destructive: "border-transparent bg-red-500 text-white hover:bg-red-600",
        outline: "text-slate-100",
        success: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
        warning: "border-amber-500/30 bg-amber-500/10 text-amber-400",
        premium: "border-transparent bg-gradient-to-r from-purple-500 to-indigo-500 text-white shadow-sm"
    }

    return (
        <div className={cn(baseStyles, variants[variant], className)} {...props} />
    )
}

export { Badge }
