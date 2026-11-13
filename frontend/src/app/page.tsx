"use client";

import React, { useState, useEffect } from "react";
import { Shield } from "lucide-react";
import { Navbar } from "../components/Navbar";
import { TransactionForm } from "../components/TransactionForm";
import { RiskGauge } from "../components/RiskGauge";
import { ExplanationCard } from "../components/ExplanationCard";
import { StatementScanner } from "../components/StatementScanner";
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
      
      {/* Top Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-sans">
            {activeTab === "single" ? "Payment fraud detection" : "Bank statement security audit"}
          </h1>
          <p className="text-xs sm:text-sm text-[var(--text-secondary)] mt-1 max-w-2xl leading-relaxed">
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
                <div className="surface-card p-10 text-center flex flex-col items-center justify-center space-y-3 border border-[var(--border-subtle)]">
                  <div className="w-12 h-12 rounded-xl bg-[var(--bg-card-raised)] border border-[var(--border-strong)] flex items-center justify-center text-[var(--text-muted)]">
                    <Shield className="h-6 w-6 stroke-[1.8]" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white">Evaluation console ready</h3>
                    <p className="text-xs text-[var(--text-secondary)] mt-1 max-w-sm leading-relaxed">
                      Enter transaction parameters on the left or select a preset scenario to score risk factors.
                    </p>
                  </div>
                </div>
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
      <footer className="border-t border-[var(--border-subtle)] bg-[var(--bg-canvas)] py-5 mt-10">
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
