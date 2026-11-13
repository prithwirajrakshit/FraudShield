"use client";

import React from "react";
import { Store, Globe, Moon, Smartphone, RefreshCw, SlidersHorizontal, ShieldCheck } from "lucide-react";
import { TransactionCheckRequest, Scenario } from "../lib/api";

interface TransactionFormProps {
  formData: TransactionCheckRequest;
  setFormData: React.Dispatch<React.SetStateAction<TransactionCheckRequest>>;
  onCheck: () => void;
  isLoading: boolean;
  scenarios: Scenario[];
}

export function TransactionForm({
  formData,
  setFormData,
  onCheck,
  isLoading,
  scenarios,
}: TransactionFormProps) {
  const quickAmounts = [15, 65, 250, 1200];

  const categories = [
    { value: "dining", label: "Dining & coffee" },
    { value: "grocery", label: "Supermarket & grocery" },
    { value: "transport", label: "Transit & fuel" },
    { value: "clothing", label: "Retail & apparel" },
    { value: "electronics", label: "Electronics & tech" },
    { value: "travel", label: "Airlines & hotels" },
    { value: "jewelry", label: "Luxury & jewelry" },
    { value: "gaming", label: "Gaming & entertainment" },
    { value: "crypto", label: "Crypto & digital assets" },
    { value: "general", label: "General merchandise" },
  ];

  const channels = [
    { value: "in_store_chip", label: "Chip & PIN" },
    { value: "contactless", label: "Contactless" },
    { value: "online", label: "Online web" },
    { value: "atm", label: "ATM cash" },
  ];

  return (
    <div className="surface-card p-6 border border-[var(--border-subtle)] space-y-6">
      
      {/* Preset Scenarios */}
      <div>
        <div className="flex items-center justify-between mb-2.5">
          <label className="text-xs font-semibold text-[var(--text-secondary)]">
            Preset test scenarios
          </label>
          <span className="text-xs text-[var(--text-muted)]">Click to load</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {scenarios.map((sc) => (
            <button
              key={sc.id}
              type="button"
              onClick={() => setFormData(sc.data)}
              className="text-left p-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] hover:border-[var(--border-strong)] hover:bg-[var(--bg-card-subtle)] transition-colors cursor-pointer"
            >
              <div className="flex items-center justify-between gap-1">
                <span className="text-xs font-medium text-white truncate">
                  {sc.name}
                </span>
                <span className="text-xs font-mono font-semibold text-[var(--accent-light)] shrink-0">
                  ₹{sc.data.amount}
                </span>
              </div>
              <p className="text-xs text-[var(--text-muted)] truncate mt-1">
                {sc.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      <div className="h-px bg-[var(--border-subtle)]" />

      {/* Main Form Fields */}
      <div className="space-y-4">
        
        {/* Amount */}
        <div>
          <label className="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">
            Transaction amount (₹ INR)
          </label>
          <div className="relative rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] focus-within:border-[var(--accent-light)] transition-colors">
            <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[var(--accent-light)] font-mono font-bold text-base">
              ₹
            </span>
            <input
              type="number"
              step="0.01"
              value={formData.amount === 0 ? "" : formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
              className="w-full pl-8 pr-4 py-2.5 text-lg font-bold font-mono text-white bg-transparent rounded-lg focus:outline-hidden"
              placeholder="0.00"
            />
          </div>

          {/* Quick pills */}
          <div className="flex gap-2 mt-2">
            {quickAmounts.map((amt) => (
              <button
                key={amt}
                type="button"
                onClick={() => setFormData({ ...formData, amount: amt })}
                className="text-xs px-2.5 py-1 rounded-md bg-[var(--bg-card-raised)] border border-[var(--border-subtle)] hover:border-[var(--border-strong)] text-[var(--text-secondary)] hover:text-white font-mono transition-colors cursor-pointer"
              >
                ₹{amt}
              </button>
            ))}
          </div>
        </div>

        {/* Merchant Name & Sector */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">
              Merchant name
            </label>
            <input
              type="text"
              value={formData.merchant_name || ""}
              onChange={(e) => setFormData({ ...formData, merchant_name: e.target.value })}
              className="w-full px-3 py-2 text-xs rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] text-white focus:border-[var(--accent-light)] focus:outline-hidden"
              placeholder="e.g. Apex Electronics"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">
              Merchant category
            </label>
            <select
              value={formData.merchant_category}
              onChange={(e) => setFormData({ ...formData, merchant_category: e.target.value })}
              className="w-full px-3 py-2 text-xs rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] text-white focus:border-[var(--accent-light)] focus:outline-hidden cursor-pointer"
            >
              {categories.map((c) => (
                <option key={c.value} value={c.value} className="bg-slate-900 text-white">
                  {c.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Payment Channel */}
        <div>
          <label className="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">
            Payment channel
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {channels.map((ch) => (
              <button
                key={ch.value}
                type="button"
                onClick={() => setFormData({ ...formData, channel: ch.value })}
                className={`py-2 px-2.5 text-xs font-medium rounded-lg border text-center transition-colors cursor-pointer ${
                  formData.channel === ch.value
                    ? "bg-[var(--accent-subtle)] border-[var(--accent-light)] text-[var(--accent-light)] font-semibold"
                    : "border-[var(--border-subtle)] bg-[var(--bg-card-raised)] text-[var(--text-secondary)] hover:text-white hover:border-[var(--border-strong)]"
                }`}
              >
                {ch.label}
              </button>
            ))}
          </div>
        </div>

        {/* Threat Signals / Contextual Toggles */}
        <div>
          <label className="block text-xs font-medium text-[var(--text-secondary)] mb-2">
            Contextual authorization signals
          </label>
          <div className="space-y-2">
            
            {/* Foreign Origin */}
            <label className="flex items-center justify-between p-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] hover:border-[var(--border-strong)] cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Globe className="h-4 w-4 text-[var(--text-muted)]" />
                <span className="text-xs text-[var(--text-secondary)]">
                  Cross-border / foreign IP address
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.is_foreign}
                onChange={(e) => setFormData({ ...formData, is_foreign: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-[var(--accent-primary)] focus:ring-[var(--accent-light)] cursor-pointer accent-[var(--accent-primary)]"
              />
            </label>

            {/* Night Time */}
            <label className="flex items-center justify-between p-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] hover:border-[var(--border-strong)] cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Moon className="h-4 w-4 text-[var(--text-muted)]" />
                <span className="text-xs text-[var(--text-secondary)]">
                  Off-peak hours (1:00 AM – 5:00 AM)
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.is_night_time}
                onChange={(e) => setFormData({ ...formData, is_night_time: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-[var(--accent-primary)] focus:ring-[var(--accent-light)] cursor-pointer accent-[var(--accent-primary)]"
              />
            </label>

            {/* Device Trust */}
            <label className="flex items-center justify-between p-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] hover:border-[var(--border-strong)] cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Smartphone className="h-4 w-4 text-[var(--text-muted)]" />
                <span className="text-xs text-[var(--text-secondary)]">
                  Recognized & trusted device
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.device_trusted}
                onChange={(e) => setFormData({ ...formData, device_trusted: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-[var(--accent-primary)] focus:ring-[var(--accent-light)] cursor-pointer accent-[var(--accent-primary)]"
              />
            </label>

          </div>
        </div>

        {/* Cardholder Baseline Average Slider */}
        <div className="p-3.5 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)]">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-medium text-[var(--text-secondary)] flex items-center gap-1.5">
              <SlidersHorizontal className="h-3.5 w-3.5 text-[var(--text-muted)]" />
              <span>Cardholder average spend</span>
            </span>
            <div className="flex items-center gap-1 px-2 py-0.5 rounded-md bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
              <span className="text-xs font-mono font-semibold text-[var(--accent-light)]">₹</span>
              <input
                type="number"
                min="1"
                value={formData.user_avg_amount === 0 ? "" : formData.user_avg_amount}
                onChange={(e) => setFormData({ ...formData, user_avg_amount: parseFloat(e.target.value) || 0 })}
                className="w-16 bg-transparent text-xs font-mono font-semibold text-white focus:outline-hidden"
                placeholder="0"
              />
            </div>
          </div>
          <input
            type="range"
            min="10"
            max="300"
            step="5"
            value={formData.user_avg_amount}
            onChange={(e) => setFormData({ ...formData, user_avg_amount: parseFloat(e.target.value) })}
            className="w-full accent-[var(--accent-primary)] cursor-pointer bg-slate-800 rounded-lg"
          />
        </div>

      </div>

      {/* Primary Action Button */}
      <button
        type="button"
        onClick={onCheck}
        disabled={isLoading || formData.amount <= 0}
        className="w-full py-3 px-4 rounded-lg bg-[var(--accent-primary)] hover:bg-[var(--accent-hover)] disabled:opacity-50 text-white font-medium text-sm transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-xs border border-[var(--accent-light)]/20"
      >
        {isLoading ? (
          <>
            <RefreshCw className="h-4 w-4 animate-spin text-white" />
            <span>Evaluating transaction...</span>
          </>
        ) : (
          <>
            <ShieldCheck className="h-4 w-4 text-white" />
            <span>Check transaction risk</span>
          </>
        )}
      </button>

    </div>
  );
}
