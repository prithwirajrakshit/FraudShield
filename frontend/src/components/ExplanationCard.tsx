"use client";

import React from "react";
import { AlertCircle, CheckCircle, ShieldCheck, ArrowRight, Lock, KeyRound, Terminal, Shield } from "lucide-react";
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
      
      {/* Detected Risk Factors & Anomaly Breakdown */}
      {riskFactors.length > 0 && (
        <div className="rounded-2xl border border-slate-800/80 glass-panel p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800/70">
            <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
              <Terminal className="h-4 w-4 text-amber-400" />
              <span>Neural Anomaly Attribution Matrix ({riskFactors.length})</span>
            </h4>
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">
              GDPR Art. 22 Compliant
            </span>
          </div>

          <div className="space-y-2.5 pt-1">
            {riskFactors.map((factor, idx) => (
              <div
                key={idx}
                className={`p-3.5 rounded-xl border transition-all ${
                  factor.type === "critical"
                    ? "bg-rose-950/40 border-rose-500/30 text-rose-200"
                    : "bg-amber-950/30 border-amber-500/30 text-amber-200"
                }`}
              >
                <div className="flex items-start gap-3">
                  <span
                    className={`h-2 w-2 rounded-full mt-1.5 shrink-0 ${
                      factor.type === "critical"
                        ? "bg-rose-500 shadow-sm shadow-rose-500/80"
                        : "bg-amber-400 shadow-sm shadow-amber-400/80"
                    }`}
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-mono font-bold tracking-tight text-white">
                        {factor.title}
                      </p>
                      <span className={`text-[10px] font-mono px-1.5 py-0.2 rounded font-semibold ${
                        factor.type === "critical" ? "bg-rose-900/60 text-rose-300" : "bg-amber-900/60 text-amber-300"
                      }`}>
                        {factor.type === "critical" ? "HIGH RISK" : "ANOMALY"}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                      {factor.detail}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Safety Alignments */}
      {safetyFactors.length > 0 && (
        <div className="rounded-2xl border border-slate-800/80 glass-panel p-5 shadow-xl">
          <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2 mb-3">
            <CheckCircle className="h-4 w-4 text-emerald-400" />
            <span>Authenticated Behavioral Baseline</span>
          </h4>
          <ul className="space-y-2">
            {safetyFactors.map((safeText, idx) => (
              <li key={idx} className="flex items-center gap-2.5 text-xs text-slate-300">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-xs shadow-emerald-400/80 shrink-0" />
                <span>{safeText}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Holographic Security Action Card */}
      <div
        className={`rounded-2xl border p-5 shadow-2xl relative overflow-hidden transition-all ${
          status === "BLOCKED"
            ? "bg-gradient-to-br from-rose-950/80 via-slate-900 to-slate-950 border-rose-500/50 text-white"
            : status === "CHALLENGE"
            ? "bg-gradient-to-br from-amber-950/80 via-slate-900 to-slate-950 border-amber-500/50 text-white"
            : "bg-gradient-to-br from-slate-900 via-slate-900/90 to-slate-950 border-cyan-500/30 text-white"
        }`}
      >
        <div className="flex items-center gap-2.5 mb-2">
          {status === "BLOCKED" ? (
            <div className="h-8 w-8 rounded-lg bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400">
              <Lock className="h-4 w-4" />
            </div>
          ) : status === "CHALLENGE" ? (
            <div className="h-8 w-8 rounded-lg bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
              <KeyRound className="h-4 w-4" />
            </div>
          ) : (
            <div className="h-8 w-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="h-4 w-4" />
            </div>
          )}
          <div>
            <h4 className="text-sm font-bold tracking-tight text-white font-mono uppercase">
              {recommendedAction.title}
            </h4>
            <span className="text-[10px] text-slate-400 font-mono">Real-Time Gateway Action Protocol</span>
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed mb-4">
          {recommendedAction.summary}
        </p>

        <div className="space-y-2 pt-3 border-t border-white/10">
          {recommendedAction.steps.map((step, idx) => (
            <div key={idx} className="flex items-start gap-2 text-xs text-slate-200">
              <ArrowRight className="h-3.5 w-3.5 text-cyan-400 mt-0.5 shrink-0" />
              <span>{step}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
