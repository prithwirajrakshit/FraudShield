"use client";

import React from "react";
import { ShieldAlert, ShieldCheck, Activity, FileSpreadsheet, Cpu } from "lucide-react";

interface NavbarProps {
  activeTab: "single" | "statement";
  setActiveTab: (tab: "single" | "statement") => void;
}

export function Navbar({ activeTab, setActiveTab }: NavbarProps) {
  return (
    <header className="border-b border-slate-800/80 bg-[#070b14]/85 backdrop-blur-xl sticky top-0 z-50 shadow-2xl shadow-blue-950/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Brand & Cyber Icon */}
        <div className="flex items-center gap-3.5">
          <div className="relative group">
            <div className="absolute -inset-1 rounded-xl bg-gradient-to-r from-blue-600 via-cyan-500 to-indigo-600 opacity-60 blur-xs group-hover:opacity-100 transition duration-500"></div>
            <div className="relative h-11 w-11 rounded-xl bg-slate-900 border border-slate-700/80 flex items-center justify-center text-cyan-400 shadow-inner">
              <ShieldCheck className="h-6 w-6 stroke-[2.2] text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-extrabold tracking-tight text-white bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text">
                FraudShield
              </span>
              <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full font-bold bg-cyan-950/80 text-cyan-300 border border-cyan-800/80">
                AI PayGuard
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono flex items-center gap-1.5">
              <span>Deep Focal Neural Shield</span>
              <span className="inline-block w-1 h-1 rounded-full bg-slate-600"></span>

            </p>
          </div>
        </div>

        {/* Futuristic Navigation Tabs */}
        <div className="flex items-center gap-1 p-1 bg-slate-900/90 rounded-xl border border-slate-800/90 shadow-inner">
          <button
            onClick={() => setActiveTab("single")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all duration-300 ${
              activeTab === "single"
                ? "bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg shadow-cyan-500/25 border border-cyan-400/40"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Activity className="h-4 w-4" />
            <span>Transaction Guard</span>
          </button>
          <button
            onClick={() => setActiveTab("statement")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all duration-300 ${
              activeTab === "statement"
                ? "bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg shadow-cyan-500/25 border border-cyan-400/40"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <FileSpreadsheet className="h-4 w-4" />
            <span>Statement Scanner</span>
          </button>
        </div>

        {/* Ambient Protection Badge (No academic jargon, purely professional trust mark) */}
        <div className="hidden md:flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 shadow-xs shadow-emerald-900/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-semibold text-emerald-300 font-mono tracking-wide">
            Bank-Grade Protection Active
          </span>
        </div>

      </div>
    </header>
  );
}
