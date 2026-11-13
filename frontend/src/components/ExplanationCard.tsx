"use client";

import React from "react";
import { CheckCircle2, ArrowRight, Lock, KeyRound, ShieldCheck } from "lucide-react";
import { RiskFactor, RecommendedAction } from "../lib/api";

interface ExplanationCardProps {
  riskFactors: RiskFactor[];
  safetyFactors: string[];
  recommendedAction: RecommendedAction;
  status: "APPROVED" | "CHALLENGE" | "BLOCKED";
}

export function ExplanationCard({
  riskFactors,
  safetyFactors,
  recommendedAction,
  status,
}: ExplanationCardProps) {
  return (
    <div className="space-y-4">
      
      {/* Identified Risk Factors */}
      {riskFactors.length > 0 && (
        <div className="surface-card p-5 border border-[var(--border-subtle)] space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
            <h4 className="text-xs font-semibold text-[var(--text-secondary)]">
              Identified risk factors ({riskFactors.length})
            </h4>
            <span className="text-xs text-[var(--text-muted)]">
              Model explanation
            </span>
          </div>

          <div className="space-y-2 pt-1">
            {riskFactors.map((factor, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border transition-colors ${
                  factor.type === "critical"
                    ? "bg-[var(--color-danger-bg)] border-[var(--color-danger-border)]"
                    : "bg-[var(--color-warning-bg)] border-[var(--color-warning-border)]"
                }`}
              >
                <div className="flex items-start gap-2.5">
                  <span
                    className={`h-2 w-2 rounded-full mt-1.5 shrink-0 ${
                      factor.type === "critical"
                        ? "bg-[var(--color-danger)]"
                        : "bg-[var(--color-warning)]"
                    }`}
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-semibold text-white">
                        {factor.title}
                      </p>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                        factor.type === "critical"
                          ? "bg-rose-900/50 text-rose-300"
                          : "bg-amber-900/50 text-amber-300"
                      }`}>
                        {factor.type === "critical" ? "Critical" : "Warning"}
                      </span>
                    </div>
                    <p className="text-xs text-[var(--text-secondary)] mt-0.5 leading-relaxed">
                      {factor.detail}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Normal Spending Indicators */}
      {safetyFactors.length > 0 && (
        <div className="surface-card p-5 border border-[var(--border-subtle)]">
          <h4 className="text-xs font-semibold text-[var(--text-secondary)] mb-2.5">
            Verified baseline indicators
          </h4>
          <ul className="space-y-1.5">
            {safetyFactors.map((safeText, idx) => (
              <li key={idx} className="flex items-center gap-2 text-xs text-[var(--text-secondary)]">
                <CheckCircle2 className="h-3.5 w-3.5 text-[var(--color-safe)] shrink-0" />
                <span>{safeText}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommended Action Card */}
      <div
        className={`surface-card p-5 border ${
          status === "BLOCKED"
            ? "border-[var(--color-danger-border)] bg-[var(--color-danger-bg)]"
            : status === "CHALLENGE"
            ? "border-[var(--color-warning-border)] bg-[var(--color-warning-bg)]"
            : "border-[var(--border-subtle)] bg-[var(--bg-card)]"
        }`}
      >
        <div className="flex items-center gap-3 mb-2">
          {status === "BLOCKED" ? (
            <div className="h-8 w-8 rounded-lg bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
              <Lock className="h-4 w-4" />
            </div>
          ) : status === "CHALLENGE" ? (
            <div className="h-8 w-8 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <KeyRound className="h-4 w-4" />
            </div>
          ) : (
            <div className="h-8 w-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="h-4 w-4" />
            </div>
          )}
          <div>
            <h4 className="text-sm font-semibold text-white">
              {recommendedAction.title}
            </h4>
            <span className="text-xs text-[var(--text-muted)]">Recommended action</span>
          </div>
        </div>

        <p className="text-xs text-[var(--text-secondary)] leading-relaxed mb-3">
          {recommendedAction.summary}
        </p>

        <div className="space-y-1.5 pt-2 border-t border-[var(--border-subtle)]">
          {recommendedAction.steps.map((step, idx) => (
            <div key={idx} className="flex items-start gap-2 text-xs text-[var(--text-secondary)]">
              <ArrowRight className="h-3.5 w-3.5 text-[var(--accent-light)] mt-0.5 shrink-0" />
              <span>{step}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
