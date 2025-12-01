import * as React from "react"

import { cn } from "@/lib/utils"

// Note: We need to install class-variance-authority for this to work elegantly
// Installing it now via command line in parallel would be good, but for now I'll implement a simpler version
// without CVA to avoid another install step blocking this, or I can just use a switch statement.
// Actually, CVA is standard for ShadcN. I should install it. 
// Let me adjust the plan to install it first.

// Wait, I can just write the classes manually for now to save time and complexity.

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link' | 'premium';
    size?: 'default' | 'sm' | 'lg' | 'icon';
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = "default", size = "default", ...props }, ref) => {

        const baseStyles = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"

        const variants = {
            default: "bg-emerald-600 text-white hover:bg-emerald-700 shadow-lg shadow-emerald-500/20",
            destructive: "bg-red-500 text-white hover:bg-red-600",
            outline: "border border-slate-700 bg-transparent hover:bg-slate-800 text-slate-100",
            secondary: "bg-slate-800 text-slate-100 hover:bg-slate-700 border border-slate-700",
            ghost: "hover:bg-slate-800 text-slate-300 hover:text-white",
            link: "text-emerald-400 underline-offset-4 hover:underline",
            premium: "bg-gradient-to-r from-emerald-500 to-teal-500 text-white hover:from-emerald-600 hover:to-teal-600 shadow-lg shadow-emerald-500/25 border-0"
        }

        const sizes = {
            default: "h-10 px-4 py-2",
            sm: "h-9 rounded-md px-3",
            lg: "h-11 rounded-md px-8",
            icon: "h-10 w-10",
        }

        return (
            <button
                className={cn(baseStyles, variants[variant], sizes[size], className)}
                ref={ref}
                {...props}
            />
        )
    }
)
Button.displayName = "Button"

export { Button }
