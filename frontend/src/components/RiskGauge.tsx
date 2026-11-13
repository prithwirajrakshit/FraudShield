"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, ShieldAlert, Clock, Cpu } from "lucide-react";
import { SecurityAssessment } from "../lib/api";

interface RiskGaugeProps {
  assessment: SecurityAssessment;
}

export function RiskGauge({ assessment }: RiskGaugeProps) {
  const percent = assessment.risk_score_percent;
  const status = assessment.status;

  // Status configuration - Clean, high-contrast, professional
  const config = {
    APPROVED: {
      color: "var(--color-safe)",
      textColor: "text-emerald-400",
      bgColor: "var(--color-safe-bg)",
      borderColor: "var(--color-safe-border)",
      badgeClass: "bg-emerald-950/60 text-emerald-300 border-emerald-500/40",
      icon: CheckCircle2,
      label: "Approved",
      summary: "Low behavioral deviation. Transaction parameters align with authenticated cardholder history."
    },
    CHALLENGE: {
      color: "var(--color-warning)",
      textColor: "text-amber-400",
      bgColor: "var(--color-warning-bg)",
      borderColor: "var(--color-warning-border)",
      badgeClass: "bg-amber-950/60 text-amber-300 border-amber-500/40",
      icon: AlertTriangle,
      label: "Verification required",
      summary: "Elevated risk signals detected. Secondary verification (such as SMS OTP) is recommended."
    },
    BLOCKED: {
      color: "var(--color-danger)",
      textColor: "text-rose-400",
      bgColor: "var(--color-danger-bg)",
      borderColor: "var(--color-danger-border)",
      badgeClass: "bg-rose-950/60 text-rose-300 border-rose-500/40",
      icon: ShieldAlert,
      label: "Transaction blocked",
      summary: "Severe anomaly detected. Payment intercepted at authorization gateway to prevent loss."
    }
  }[status];

  const IconComponent = config.icon;

  // SVG Radial Geometry
  const radius = 64;
  const strokeWidth = 10;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percent / 100) * circumference;

  return (
    <div className="surface-card p-6 border border-[var(--border-subtle)]">
      <div className="flex flex-col sm:flex-row items-center gap-6 justify-between">
        
        {/* Precision Circular Risk Meter */}
        <div className="relative flex items-center justify-center shrink-0">
          <svg className="w-36 h-36 transform -rotate-90" aria-label={`Risk meter: ${percent}%`}>
            {/* Background Track */}
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke="#1e293b"
              strokeWidth={strokeWidth}
              fill="transparent"
            />
            {/* Active Value Arc */}
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke={config.color}
              strokeWidth={strokeWidth}
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className="transition-[stroke-dashoffset] duration-500 ease-out"
            />
          </svg>

          {/* Central Metric */}
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold tracking-tight text-white font-mono">
              {percent}%
            </span>
            <span className="text-xs text-[var(--text-muted)] font-medium">
              Threat score
            </span>
          </div>
        </div>

        {/* Assessment Details */}
        <div className="flex-1 text-center sm:text-left space-y-3">
          
          <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${config.badgeClass}`}>
              <IconComponent className="h-3.5 w-3.5" />
              <span>{config.label}</span>
            </span>

            <span className="inline-flex items-center gap-1.5 text-xs text-[var(--text-secondary)] bg-[var(--bg-card-raised)] px-2.5 py-1 rounded-md border border-[var(--border-subtle)] font-mono">
              <Clock className="h-3 w-3 text-[var(--text-muted)]" />
              <span>{assessment.latency_ms} ms</span>
            </span>

            <span className="inline-flex items-center gap-1.5 text-xs text-[var(--text-secondary)] bg-[var(--bg-card-raised)] px-2.5 py-1 rounded-md border border-[var(--border-subtle)]">
              <Cpu className="h-3 w-3 text-[var(--text-muted)]" />
              <span>Neural evaluation</span>
            </span>
          </div>

          <h3 className={`text-xl font-bold tracking-tight ${config.textColor}`}>
            {assessment.headline}
          </h3>

          <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
            {config.summary}
          </p>
        </div>

      </div>
    </div>
  );
}
