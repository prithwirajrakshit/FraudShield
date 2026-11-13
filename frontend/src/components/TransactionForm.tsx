"use client";

import React from "react";
import { IndianRupee, Store, Globe, Moon, Smartphone, RefreshCw, Sparkles, SlidersHorizontal, Shield } from "lucide-react";
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
    { value: "dining", label: "Dining & Coffee" },
    { value: "grocery", label: "Supermarket / Grocery" },
    { value: "transport", label: "Transit & Fuel" },
    { value: "clothing", label: "Retail & Apparel" },
    { value: "electronics", label: "Electronics & Tech" },
    { value: "travel", label: "Airlines & Hotels" },
    { value: "jewelry", label: "Luxury & Jewelry" },
    { value: "gaming", label: "Gaming & Entertainment" },
    { value: "crypto", label: "Crypto / Digital Asset" },
    { value: "general", label: "General Merchandise" },
  ];

  const channels = [
    { value: "in_store_chip", label: "In-Store Chip & PIN" },
    { value: "contactless", label: "Contactless Tap" },
    { value: "online", label: "Online Web Checkout" },
    { value: "atm", label: "Cash" },
  ];

  const loadScenario = (sc: Scenario) => {
    setFormData(sc.data);
  };

  return (
    <div className="rounded-2xl border border-slate-800/80 glass-panel p-6 shadow-2xl space-y-6">
      
      {/* Scenario Presets */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-1.5 text-xs font-mono font-bold uppercase tracking-wider text-cyan-400">
            <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
            <span>Telemetry Simulation Presets</span>
          </div>
          <span className="text-[10px] font-mono text-slate-500">Instant Load</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {scenarios.map((sc) => (
            <button
              key={sc.id}
              type="button"
              onClick={() => loadScenario(sc)}
              className="text-left p-3 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800/80 hover:border-cyan-500/50 transition-all duration-300 group cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <p className="text-xs font-bold text-slate-200 group-hover:text-cyan-300 transition-colors">
                  {sc.name}
                </p>
                <span className="text-[10px] font-mono text-cyan-400 font-bold bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-800/60">
                  ₹{sc.data.amount}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 truncate mt-1">
                {sc.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      <hr className="border-slate-800/80" />

      {/* Main Form Fields */}
      <div className="space-y-4">
        
        {/* Amount */}
        <div>
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-1.5">
            Transaction Amount (₹)
          </label>
          <div className="relative rounded-xl border border-slate-800 bg-slate-950 focus-within:border-cyan-500 focus-within:ring-2 focus-within:ring-cyan-500/20 transition-all">
            <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-cyan-400 font-mono font-bold text-lg">
              ₹
            </span>
            <input
              type="number"
              step="0.01"
              value={formData.amount === 0 ? "" : formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
              className="w-full pl-8 pr-4 py-3 text-xl font-bold font-mono text-white bg-transparent rounded-xl focus:outline-hidden"
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
                className="text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-800 text-slate-300 font-mono font-medium transition-colors cursor-pointer"
              >
                ₹{amt}
              </button>
            ))}
          </div>
        </div>

        {/* Merchant Name & Category */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Merchant Name
            </label>
            <input
              type="text"
              value={formData.merchant_name || ""}
              onChange={(e) => setFormData({ ...formData, merchant_name: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-800 bg-slate-950 text-white focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 focus:outline-hidden"
              placeholder="e.g. Apex Store"
            />
          </div>

          <div>
            <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Merchant Sector
            </label>
            <select
              value={formData.merchant_category}
              onChange={(e) => setFormData({ ...formData, merchant_category: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-800 bg-slate-950 text-white focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 focus:outline-hidden"
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
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-1.5">
            Channel Protocol
          </label>
          <div className="grid grid-cols-2 gap-2">
            {channels.map((ch) => (
              <button
                key={ch.value}
                type="button"
                onClick={() => setFormData({ ...formData, channel: ch.value })}
                className={`py-2 px-3 text-xs font-medium rounded-xl border text-center transition-all cursor-pointer ${
                  formData.channel === ch.value
                    ? "bg-cyan-950/70 border-cyan-500 text-cyan-300 font-bold shadow-md shadow-cyan-950/50"
                    : "border-slate-800 bg-slate-950 text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                }`}
              >
                {ch.label}
              </button>
            ))}
          </div>
        </div>

        {/* Contextual Risk Indicators (Cyber Switches) */}
        <div>
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-2">
            Contextual Threat Signals
          </label>
          <div className="space-y-2">
            
            {/* Foreign Origin */}
            <label className="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950 hover:bg-slate-900/80 cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Globe className="h-4 w-4 text-cyan-400" />
                <span className="text-xs font-semibold text-slate-200">
                  Cross-Border / Foreign IP Origin
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.is_foreign}
                onChange={(e) => setFormData({ ...formData, is_foreign: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-400 cursor-pointer accent-cyan-500"
              />
            </label>

            {/* Night Time */}
            <label className="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950 hover:bg-slate-900/80 cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Moon className="h-4 w-4 text-indigo-400" />
                <span className="text-xs font-semibold text-slate-200">
                  Off-Peak Hours (1:00 AM – 5:00 AM)
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.is_night_time}
                onChange={(e) => setFormData({ ...formData, is_night_time: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-400 cursor-pointer accent-cyan-500"
              />
            </label>

            {/* Device Trust */}
            <label className="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950 hover:bg-slate-900/80 cursor-pointer transition-colors">
              <div className="flex items-center gap-2.5">
                <Smartphone className="h-4 w-4 text-emerald-400" />
                <span className="text-xs font-semibold text-slate-200">
                  Authenticated / Known Device
                </span>
              </div>
              <input
                type="checkbox"
                checked={formData.device_trusted}
                onChange={(e) => setFormData({ ...formData, device_trusted: e.target.checked })}
                className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-400 cursor-pointer accent-cyan-500"
              />
            </label>

          </div>
        </div>

        {/* Cardholder Baseline Average Slider */}
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-950">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <SlidersHorizontal className="h-3.5 w-3.5 text-cyan-400" />
              <span>Cardholder Historical Average</span>
            </span>
            <div className="flex items-center gap-1 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">
              <span className="text-xs font-mono font-bold text-cyan-400">₹</span>
              <input
                type="number"
                min="1"
                value={formData.user_avg_amount === 0 ? "" : formData.user_avg_amount}
                onChange={(e) => setFormData({ ...formData, user_avg_amount: parseFloat(e.target.value) || 0 })}
                className="w-16 bg-transparent text-xs font-mono font-bold text-cyan-300 focus:outline-none"
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
            className="w-full accent-cyan-400 cursor-pointer bg-slate-800 rounded-lg"
          />
        </div>

      </div>

      {/* Cyber Authorization Action Button */}
      <button
        type="button"
        onClick={onCheck}
        disabled={isLoading || formData.amount <= 0}
        className="w-full py-4 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-cyan-500 to-indigo-600 hover:from-blue-500 hover:to-cyan-400 disabled:opacity-50 text-white font-mono font-bold text-xs uppercase tracking-wider shadow-lg shadow-cyan-500/25 border border-cyan-400/40 transition-all duration-300 flex items-center justify-center gap-2.5 cursor-pointer"
      >
        {isLoading ? (
          <>
            <RefreshCw className="h-4 w-4 animate-spin text-white" />
            <span>Scanning Behavioral Embeddings...</span>
          </>
        ) : (
          <>
            <Shield className="h-4 w-4 text-white" />
            <span>Verify Transaction Security</span>
          </>
        )}
      </button>

    </div>
  );
}
