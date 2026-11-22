"use client";

import React from "react";
import { Shield, Activity, FileSpreadsheet } from "lucide-react";

interface NavbarProps {
  activeTab: "single" | "statement";
  setActiveTab: (tab: "single" | "statement") => void;
}

export function Navbar({ activeTab, setActiveTab }: NavbarProps) {
  return (
    <header className="border-b border-[var(--border-subtle)] bg-[var(--bg-canvas)]/95 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand identity: Clean, confident, authoritative */}
        <div className="flex items-center gap-3">
          <div
            className="h-9 w-9 rounded-lg border flex items-center justify-center text-rose-400 logo-red-glow"
            aria-label="FraudShield Sentinel Shield"
          >
            <Shield className="h-5 w-5 stroke-[2] logo-red-icon" />
          </div>
          <div>
            <span
              className="text-base font-bold text-white block leading-tight tracking-wider"
              style={{ fontFamily: "var(--font-display)" }}
            >
              FraudShield
            </span>
            <p className="text-xs text-[var(--text-muted)] leading-none mt-1">
              Payment security & risk analysis
            </p>
          </div>
        </div>

        {/* Segmented Control Navigation */}
        <nav aria-label="Console navigation">
          <div className="flex items-center p-1 bg-[var(--bg-card)] rounded-lg border border-[var(--border-subtle)]">
            <button
              type="button"
              onClick={() => setActiveTab("single")}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-medium cursor-pointer ${
                activeTab === "single"
                  ? "glow-subcard-active text-white"
                  : "text-[var(--text-secondary)] hover:text-white hover:bg-[var(--bg-card-raised)]/50"
              }`}
            >
              <Activity className="h-3.5 w-3.5 text-[var(--accent-light)]" />
              <span>Live transaction</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("statement")}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-medium cursor-pointer ${
                activeTab === "statement"
                  ? "glow-subcard-active text-white"
                  : "text-[var(--text-secondary)] hover:text-white hover:bg-[var(--bg-card-raised)]/50"
              }`}
            >
              <FileSpreadsheet className="h-3.5 w-3.5 text-[var(--accent-light)]" />
              <span>Statement scanner</span>
            </button>
          </div>
        </nav>

        {/* Protection state badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full glow-pill-safe">
          <span className="h-2 w-2 rounded-full bg-[var(--color-safe)] glow-icon-safe" />
          <span className="text-xs font-medium text-[var(--color-safe)]">
            System active
          </span>
        </div>

      </div>
    </header>
  );
}
