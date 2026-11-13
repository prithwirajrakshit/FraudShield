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
          <div className="h-9 w-9 rounded-lg bg-[var(--bg-card-raised)] border border-[var(--border-strong)] flex items-center justify-center text-[var(--accent-light)]">
            <Shield className="h-5 w-5 stroke-[2]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-bold tracking-tight text-white font-sans">
                FraudShield
              </span>
              <span className="text-xs px-2 py-0.5 rounded-md font-medium bg-[var(--bg-card-subtle)] text-[var(--text-secondary)] border border-[var(--border-subtle)]">
                v1.0
              </span>
            </div>
            <p className="text-xs text-[var(--text-muted)] leading-none mt-0.5">
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
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-medium transition-colors cursor-pointer ${
                activeTab === "single"
                  ? "bg-[var(--bg-card-raised)] text-white shadow-xs border border-[var(--border-strong)]"
                  : "text-[var(--text-secondary)] hover:text-white hover:bg-[var(--bg-card-raised)]/50"
              }`}
            >
              <Activity className="h-3.5 w-3.5 text-[var(--accent-light)]" />
              <span>Live transaction</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("statement")}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-medium transition-colors cursor-pointer ${
                activeTab === "statement"
                  ? "bg-[var(--bg-card-raised)] text-white shadow-xs border border-[var(--border-strong)]"
                  : "text-[var(--text-secondary)] hover:text-white hover:bg-[var(--bg-card-raised)]/50"
              }`}
            >
              <FileSpreadsheet className="h-3.5 w-3.5 text-[var(--accent-light)]" />
              <span>Statement scanner</span>
            </button>
          </div>
        </nav>

        {/* Protection state badge: quiet, professional, no pinging animations */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--color-safe-bg)] border border-[var(--color-safe-border)]">
          <span className="h-2 w-2 rounded-full bg-[var(--color-safe)]" />
          <span className="text-xs font-medium text-[var(--color-safe)]">
            System active
          </span>
        </div>

      </div>
    </header>
  );
}
