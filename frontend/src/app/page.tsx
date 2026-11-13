"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck } from "lucide-react";
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

  // Initial Form State - Clean slate (amount 0)
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

  // Assessment State (starts null until evaluated)
  const [assessmentResult, setAssessmentResult] = useState<TransactionCheckResponse | null>(null);

  // Load scenarios on mount without auto-evaluating
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

  const status = assessmentResult?.security_assessment.status || "APPROVED";
  const glowColorClass =
    status === "BLOCKED"
      ? "from-rose-600/15 via-rose-950/5 to-transparent"
      : status === "CHALLENGE"
      ? "from-amber-600/15 via-amber-950/5 to-transparent"
      : "from-cyan-600/15 via-blue-950/5 to-transparent";

  return (
    <div className="relative min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans cyber-grid selection:bg-cyan-500/30 selection:text-cyan-200">
      
      {/* Dynamic Ambient Background Glow Light Orb */}
      <div className={`fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[450px] bg-gradient-to-b ${glowColorClass} blur-[120px] pointer-events-none transition-all duration-700`}></div>

      {/* Top Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        
        {/* Page Hero Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-2">
            <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping"></span>
            <span className="text-[11px] font-mono uppercase tracking-widest text-cyan-400 font-bold">
              Autonomous Threat Interception Gateway
            </span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-black tracking-tight text-white font-mono">
            {activeTab === "single" ? (
              <>
                Real-Time <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-300 bg-clip-text text-transparent">Payment Security</span> Guard
              </>
            ) : (
              <>
                Bank & Card <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-300 bg-clip-text text-transparent">Statement Security</span> Scanner
              </>
            )}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl leading-relaxed">
            {activeTab === "single"
              ? "Verify individual purchase authorizations against high-dimensional behavioral anomaly patterns with sub-2ms PyTorch neural inference."
              : "Bulk-scan cardholder and corporate statements. Detect unauthorized account takeover, overseas cash-outs, and rapid fund drain."}
          </p>
        </div>

        {/* Tab 1: Single Transaction Guard */}
        {activeTab === "single" && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Column: Form & Simulator Inputs (5 cols) */}
            <div className="lg:col-span-5">
              <TransactionForm
                formData={formData}
                setFormData={setFormData}
                onCheck={() => handleCheck(formData)}
                isLoading={isLoading}
                scenarios={scenarios}
              />
            </div>

            {/* Right Column: Holographic Risk Gauge & XAI Attribution (7 cols) */}
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
                <div className="rounded-2xl border border-slate-800/80 glass-panel p-12 text-center flex flex-col items-center justify-center space-y-4">
                  <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-cyan-400">
                    <ShieldCheck className="h-8 w-8" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white font-mono">Autonomous Threat Gateway Ready</h3>
                    <p className="text-xs text-slate-400 mt-1 max-w-sm leading-relaxed">
                      Enter transaction parameters on the left or select a preset scenario to evaluate with sub-2ms PyTorch neural inference.
                    </p>
                  </div>
                </div>
              )}
            </div>

          </div>
        )}

        {/* Tab 2: Statement Bulk Scanner */}
        {activeTab === "statement" && (
          <div className="max-w-5xl mx-auto">
            <StatementScanner />
          </div>
        )}

      </main>

      {/* Cyber Footer */}
      <footer className="relative z-10 border-t border-slate-800/80 bg-[#070b14]/90 backdrop-blur-md py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-slate-500 gap-3">
          <p>© 2026 FraudShield AI • Adaptive Deep Focal Neural Security Architecture</p>
          <div className="flex items-center gap-5">
            <span className="flex items-center gap-1.5 text-slate-400">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-xs shadow-emerald-400"></span>
              256-Bit Hardware Encryption
            </span>
            <span className="text-slate-400">GDPR Art. 22 Audited</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
