"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, ShieldAlert, Zap, Cpu, Radio } from "lucide-react";
import { SecurityAssessment } from "../lib/api";

interface RiskGaugeProps {
  assessment: SecurityAssessment;
}

export function RiskGauge({ assessment }: RiskGaugeProps) {
  const percent = assessment.risk_score_percent;
  const status = assessment.status;

  // Futuristic status configurations
  const config = {
    APPROVED: {
      color: "#10b981", // Emerald neon
      glowClass: "from-emerald-500/20 via-emerald-950/10 to-transparent",
      borderColor: "border-emerald-500/40",
      textColor: "text-emerald-400",
      badgeClass: "bg-emerald-950/80 text-emerald-300 border-emerald-500/60 shadow-lg shadow-emerald-950/50",
      glowHex: "#10b981",
      icon: CheckCircle2,
      label: "Safe to Authorize",
      description: "Low-entropy behavioral signal. Parameters align with authenticated cardholder history."
    },
    CHALLENGE: {
      color: "#f59e0b", // Amber solar
      glowClass: "from-amber-500/20 via-amber-950/10 to-transparent",
      borderColor: "border-amber-500/40",
      textColor: "text-amber-400",
      badgeClass: "bg-amber-950/80 text-amber-300 border-amber-500/60 shadow-lg shadow-amber-950/50",
      glowHex: "#f59e0b",
      icon: AlertTriangle,
      label: "Verification Required",
      description: "Elevated risk signals detected. Requires two-factor SMS passcode authentication."
    },
    BLOCKED: {
      color: "#f43f5e", // Crimson cyber laser
      glowClass: "from-rose-500/25 via-rose-950/15 to-transparent",
      borderColor: "border-rose-500/50",
      textColor: "text-rose-400",
      badgeClass: "bg-rose-950/90 text-rose-300 border-rose-500/80 shadow-lg shadow-rose-950/60",
      glowHex: "#f43f5e",
      icon: ShieldAlert,
      label: "Fraud Intercepted",
      description: "Severe threat anomaly detected. Transaction intercepted at gateway to protect account funds."
    }
  }[status];

  const IconComponent = config.icon;

  // SVG Radial Geometry
  const radius = 72;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percent / 100) * circumference;

  return (
    <div className={`relative overflow-hidden rounded-2xl border ${config.borderColor} glass-panel p-6 shadow-2xl transition-all duration-500`}>
      {/* Ambient Radial Glow Lighting in Background */}
      <div className={`absolute -top-24 -right-24 w-72 h-72 rounded-full bg-gradient-to-br ${config.glowClass} blur-3xl pointer-events-none`}></div>
      <div className={`absolute -bottom-24 -left-24 w-72 h-72 rounded-full bg-gradient-to-tr ${config.glowClass} blur-3xl pointer-events-none`}></div>

      <div className="relative z-10 flex flex-col md:flex-row items-center gap-7 justify-between">
        
        {/* Holographic Circular HUD Gauge */}
        <div className="relative flex items-center justify-center shrink-0">
          
          {/* Subtle Outer Radar Tick Ring */}
          <div className="absolute inset-0 rounded-full border border-dashed border-slate-700/60 scale-110"></div>
          
          <svg className="w-44 h-44 transform -rotate-90">
            {/* SVG Filter for Neon Glow */}
            <defs>
              <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Background Track */}
            <circle
              cx="88"
              cy="88"
              r={radius}
              stroke="#1e293b"
              strokeWidth="12"
              fill="transparent"
              strokeDasharray="4 6"
            />

            {/* Glowing Active Progress Arc */}
            <circle
              cx="88"
              cy="88"
              r={radius}
              stroke={config.color}
              strokeWidth="12"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              filter="url(#neon-glow)"
              className="transition-all duration-700 ease-out"
            />
          </svg>

          {/* Central Digital Matrix Readout */}
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-black tracking-tight text-white font-mono drop-shadow-md">
              {percent}%
            </span>
            <span className="text-[10px] font-bold tracking-widest uppercase text-slate-400 flex items-center gap-1 mt-0.5">
              <Radio className="h-2.5 w-2.5 text-cyan-400 animate-pulse" />
              Threat Index
            </span>
          </div>
        </div>

        {/* Telemetry & Assessment Readout */}
        <div className="flex-1 text-center md:text-left space-y-3">
          
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2.5">
            <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${config.badgeClass}`}>
              <IconComponent className="h-3.5 w-3.5 stroke-[2.5]" />
              {status}
            </span>

            <span className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-slate-300 bg-slate-900/90 px-3 py-1 rounded-full border border-slate-700/80">
              <Zap className="h-3 w-3 text-cyan-400 fill-cyan-400" />
              <span>Inference: {assessment.latency_ms}ms</span>
            </span>

            <span className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-slate-400 bg-slate-900/90 px-3 py-1 rounded-full border border-slate-700/80">
              <Cpu className="h-3 w-3 text-indigo-400" />
              <span>Focal Neural Engine</span>
            </span>
          </div>

          <h3 className={`text-2xl font-extrabold tracking-tight ${config.textColor}`}>
            {assessment.headline}
          </h3>

          <p className="text-sm text-slate-300 leading-relaxed max-w-xl">
            {config.description}
          </p>
        </div>

      </div>
    </div>
  );
}
