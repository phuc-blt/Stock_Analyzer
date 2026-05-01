'use client';

import { TrendingUp, BarChart3, Brain, Activity, DollarSign, TrendingDown } from 'lucide-react';

export function BackgroundIcons() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none">
      {/* Grid pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-[0.02] dark:opacity-[0.03]" />
      
      {/* Floating icons */}
      <div className="absolute top-20 left-10 text-blue-500/10 dark:text-blue-400/10 animate-float">
        <TrendingUp className="h-24 w-24" />
      </div>
      
      <div className="absolute top-40 right-20 text-green-500/10 dark:text-green-400/10 animate-float-delayed">
        <BarChart3 className="h-32 w-32" />
      </div>
      
      <div className="absolute bottom-32 left-20 text-purple-500/10 dark:text-purple-400/10 animate-float">
        <Brain className="h-28 w-28" />
      </div>
      
      <div className="absolute top-60 right-40 text-orange-500/10 dark:text-orange-400/10 animate-float-delayed">
        <Activity className="h-20 w-20" />
      </div>
      
      <div className="absolute bottom-20 right-10 text-yellow-500/10 dark:text-yellow-400/10 animate-float">
        <DollarSign className="h-24 w-24" />
      </div>
      
      <div className="absolute top-80 left-1/2 text-red-500/10 dark:text-red-400/10 animate-float-delayed">
        <TrendingDown className="h-16 w-16" />
      </div>
      
      {/* Gradient overlays */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/20 via-transparent to-purple-50/20 dark:from-blue-900/10 dark:via-transparent dark:to-purple-900/10" />
    </div>
  );
}
