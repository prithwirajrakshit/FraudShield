"use client";

import React, { useState, useEffect } from "react";
import { Shield } from "lucide-react";
import { Navbar } from "../components/Navbar";
import { TransactionForm } from "../components/TransactionForm";
import { RiskGauge } from "../components/RiskGauge";
import { ExplanationCard } from "../components/ExplanationCard";
import { StatementScanner } from "../components/StatementScanner";
import { GlowCard } from "../components/GlowCard";
import {
  TransactionCheckRequest,
  TransactionCheckResponse,
  Scenario,
  checkTransaction,
  fetchScenarios,
} from "../lib/api";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"single" | "statement">("single");
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Initial Form State
  const [formData, setFormData] = useState<TransactionCheckRequest>({
    amount: 0,
    merchant_name: "",
    merchant_category: "dining",
    channel: "online",
    is_foreign: false,
    is_night_time: false,
    device_trusted: true,
    user_avg_amount: 50.0,
    velocity_1h: 1,
  });

  // Assessment State
  const [assessmentResult, setAssessmentResult] = useState<TransactionCheckResponse | null>(null);

  useEffect(() => {
    async function init() {
      const scList = await fetchScenarios();
      setScenarios(scList);
    }
    init();
  }, []);

  const handleCheck = async (dataToCheck = formData) => {
    setIsLoading(true);
    try {
      const res = await checkTransaction(dataToCheck);
      setAssessmentResult(res);
    } catch (e) {
      console.error("Evaluation error:", e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-canvas)] text-[var(--text-primary)] flex flex-col font-sans app-grid-bg">
      {/* High-Fidelity Atmospheric Depth & Telemetry Grid Mesh */}
      <div className="app-ambient-glow" aria-hidden="true" />
      <div className="app-grid-mesh" aria-hidden="true" />
      
      {/* Cascading Security Telemetry Flow (Slow Top-to-Bottom Ambient Glow) */}
      <div className="app-flow-container" aria-hidden="true">
        <div className="app-flow-track">
          <div className="app-flow-aurora" />
        </div>
      </div>
      
      {/* Top Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full relative z-10">
        
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-xl sm:text-2xl font-bold text-white font-display">
            {activeTab === "single" ? "Payment fraud detection" : "Bank statement security audit"}
          </h1>
          <p className="text-xs sm:text-sm text-[var(--text-secondary)] mt-1.5 max-w-2xl leading-relaxed">
            {activeTab === "single"
              ? "Score live purchase authorizations against behavioral anomaly patterns in real time."
              : "Scan bank and card statements to identify suspicious charges, velocity spikes, and off-hour withdrawals."}
          </p>
        </div>

        {/* Tab 1: Single Transaction Guard */}
        {activeTab === "single" && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* Left Column: Form (5 cols) */}
            <div className="lg:col-span-5">
              <TransactionForm
                formData={formData}
                setFormData={setFormData}
                onCheck={() => handleCheck(formData)}
                isLoading={isLoading}
                scenarios={scenarios}
              />
            </div>

            {/* Right Column: Assessment & Breakdown (7 cols) */}
            <div className="lg:col-span-7 space-y-6">
              {assessmentResult ? (
                <>
                  <RiskGauge assessment={assessmentResult.security_assessment} />

                  <ExplanationCard
                    riskFactors={assessmentResult.explanation.risk_factors}
                    safetyFactors={assessmentResult.explanation.safety_factors}
                    recommendedAction={assessmentResult.explanation.recommended_action}
                    status={assessmentResult.security_assessment.status}
                  />
                </>
              ) : (
                <GlowCard className="min-h-[420px] flex flex-col justify-center">
                  <div className="p-8 sm:p-12 text-center flex flex-col items-center justify-center space-y-4 w-full">
                    {/* Centered Luminous Cyber Shield Badge */}
                    <div className="w-16 h-16 rounded-2xl glow-badge-cyber flex items-center justify-center">
                      <Shield className="h-8 w-8 stroke-[2] glow-icon-cyber" />
                    </div>

                    <div className="max-w-md">
                      <h3 className="text-base font-bold text-white font-display tracking-wide">
                        Evaluation console ready
                      </h3>
                      <p className="text-xs text-[var(--text-secondary)] mt-1.5 leading-relaxed">
                        Enter transaction parameters on the left or select a preset scenario to score risk factors in real time.
                      </p>
                    </div>

                    {/* Readiness Status Indicators */}
                    <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium glow-pill-safe">
                        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 motion-safe:animate-pulse" />
                        Gateway active
                      </span>
                      <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] text-[var(--text-secondary)] bg-[var(--bg-card-raised)] border border-sky-500/30">
                        Baseline loaded
                      </span>
                    </div>
                  </div>
                </GlowCard>
              )}
            </div>

          </div>
        )}

        {/* Tab 2: Statement Scanner */}
        {activeTab === "statement" && (
          <div className="max-w-4xl mx-auto">
            <StatementScanner />
          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="border-t border-[var(--border-subtle)] bg-[var(--bg-canvas)]/90 backdrop-blur-xs py-5 mt-10 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-[var(--text-muted)] gap-2">
          <p>© 2026 FraudShield • Payment risk scoring & anomaly detection console</p>
          <div className="flex items-center gap-4">
            <span className="text-[var(--text-secondary)]">
              Ephemeral in-memory processing
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
