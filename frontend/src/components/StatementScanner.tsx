"use client";

import React, { useState } from "react";
import { Upload, FileText, CheckCircle2, AlertTriangle, ShieldAlert, Sparkles, RefreshCw, Lock, Eye, EyeOff, KeyRound } from "lucide-react";
import { StatementScanResponse, uploadStatement } from "../lib/api";

export function StatementScanner() {
  const [file, setFile] = useState<File | null>(null);
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState(false);
  const [scanResult, setScanResult] = useState<StatementScanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [passwordErrorType, setPasswordErrorType] = useState<"required" | "incorrect" | null>(null);

  // Modal Dialog States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalType, setModalType] = useState<"required" | "incorrect">("required");
  const [modalPwd, setModalPwd] = useState("");
  const [modalShowPwd, setModalShowPwd] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setPasswordErrorType(null);
    }
  };

  const runScan = async (targetFile: File, overridePassword?: string) => {
    setIsLoading(true);
    setError(null);
    setPasswordErrorType(null);
    const activePassword = overridePassword !== undefined ? overridePassword : password;

    try {
      const data = await uploadStatement(targetFile, activePassword);
      setScanResult(data);
      setPasswordErrorType(null);
      setIsModalOpen(false);
    } catch (err: any) {
      const errType = err.errorType;
      const msg = err?.message || "Failed to process statement.";
      setError(msg);

      if (errType === "PASSWORD_REQUIRED" || msg.toLowerCase().includes("password-protected") || msg.toLowerCase().includes("password required")) {
        setPasswordErrorType("required");
        setModalType("required");
        setModalPwd("");
        setIsModalOpen(true);
      } else if (errType === "PASSWORD_INCORRECT" || (msg.toLowerCase().includes("incorrect") && msg.toLowerCase().includes("password"))) {
        setPasswordErrorType("incorrect");
        setModalType("incorrect");
        setModalPwd(activePassword);
        setIsModalOpen(true);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleModalSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!modalPwd.trim() || !file) return;
    const clean = modalPwd.trim();
    setPassword(clean);
    setIsModalOpen(false);
    runScan(file, clean);
  };

  const loadSampleStatement = () => {
    const csvContent = `date,merchant,category,amount,channel
2026-10-28,Blue Bottle Coffee,dining,4.75,contactless
2026-10-28,Trader Joe's Groceries,grocery,64.20,in_store_chip
2026-10-29,Shell Gas Station,transport,42.00,in_store_chip
2026-10-29,Netflix Subscription,general,15.99,online
2026-10-30,Target Department Store,clothing,78.50,in_store_chip
2026-10-31,Subway Restaurant,dining,11.40,contactless
2026-11-01,Binance Intl Crypto Exchange,crypto,1850.00,online
2026-11-01,Night ATM-Midnight Cash Out,general,400.00,atm
2026-11-02,Apple Store Online,electronics,1299.00,online`;

    const blob = new Blob([csvContent], { type: "text/csv" });
    const sampleFile = new File([blob], "sample_bank_statement.csv", { type: "text/csv" });
    setFile(sampleFile);
    setPassword("");
    runScan(sampleFile);
  };

  return (
    <div className="space-y-6">
      
      {/* Upload Zone */}
      <div className="surface-card p-8 text-center border-2 border-dashed border-[var(--border-subtle)] hover:border-[var(--border-strong)] transition-colors">
        <div className="max-w-xl mx-auto space-y-4">
          
          <div className="h-12 w-12 rounded-xl bg-[var(--bg-card-raised)] border border-[var(--border-strong)] flex items-center justify-center text-[var(--accent-light)] mx-auto">
            <Upload className="h-6 w-6 stroke-[2]" />
          </div>

          <div>
            <h3 className="text-base font-bold text-white font-sans">
              Upload bank statement
            </h3>
            <p className="text-xs text-[var(--text-secondary)] mt-1">
              Supports CSV, PDF, Excel (.xlsx, .xls), and encrypted ZIP files up to 25 MB.
            </p>
          </div>

          {/* Password Input for Protected Statements */}
          <div className="p-3.5 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] text-left">
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-medium text-[var(--text-secondary)] flex items-center gap-1.5">
                <Lock className="h-3.5 w-3.5 text-[var(--text-muted)]" />
                <span>Statement password (if encrypted)</span>
              </label>
              <span className="text-[10px] text-[var(--text-muted)]">Optional</span>
            </div>
            
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (passwordErrorType) setPasswordErrorType(null);
                  if (error) setError(null);
                }}
                placeholder="e.g. DOB (DDMMYYYY), PAN, or mobile number"
                className="w-full px-3 py-2 pr-10 text-xs rounded-md border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-white placeholder-[var(--text-muted)] focus:border-[var(--accent-light)] focus:outline-hidden"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-[var(--text-muted)] hover:text-white cursor-pointer"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-2.5 pt-1">
            <label className="px-4 py-2 rounded-lg bg-[var(--accent-primary)] hover:bg-[var(--accent-hover)] text-white font-medium text-xs transition-colors cursor-pointer border border-[var(--accent-light)]/20 shadow-xs">
              Select statement file
              <input
                type="file"
                accept=".csv,.zip,.xlsx,.xls,.pdf"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>

            <button
              type="button"
              onClick={loadSampleStatement}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-[var(--bg-card-raised)] border border-[var(--border-subtle)] hover:border-[var(--border-strong)] text-[var(--text-secondary)] hover:text-white font-medium text-xs transition-colors cursor-pointer"
            >
              <Sparkles className="h-3.5 w-3.5 text-[var(--accent-light)]" />
              <span>Load demo statement</span>
            </button>
          </div>

          {file && (
            <div className="mt-2 inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[var(--bg-card-raised)] border border-[var(--border-subtle)] text-xs text-[var(--accent-light)] font-mono">
              <FileText className="h-3.5 w-3.5" />
              <span>{file.name}</span>
              <button
                type="button"
                onClick={() => runScan(file)}
                disabled={isLoading}
                className="ml-2 font-semibold text-white hover:underline cursor-pointer"
              >
                {isLoading ? "Scanning..." : "Scan now"}
              </button>
            </div>
          )}

          {error && (
            <div className="p-3 rounded-lg border border-[var(--color-danger-border)] bg-[var(--color-danger-bg)] text-xs text-rose-300 flex items-start gap-2.5 text-left">
              <KeyRound className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Processing notice</p>
                <p className="text-rose-200 mt-0.5">{error}</p>
              </div>
            </div>
          )}

        </div>
      </div>

      {/* Loading Readout */}
      {isLoading && (
        <div className="py-8 text-center space-y-2 surface-card border border-[var(--border-subtle)]">
          <RefreshCw className="h-5 w-5 text-[var(--accent-light)] animate-spin mx-auto" />
          <p className="text-xs text-[var(--text-secondary)]">
            Scanning statement against fraud detection model...
          </p>
        </div>
      )}

      {/* Results View */}
      {scanResult && !isLoading && (
        <div className="space-y-6">
          
          {/* Summary Stat Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            
            <div className="surface-card p-4 border border-[var(--border-subtle)]">
              <span className="text-xs text-[var(--text-muted)] font-medium">
                Scanned transactions
              </span>
              <p className="text-2xl font-bold font-mono text-white mt-1">
                {scanResult.summary.total_transactions}
              </p>
              <span className="text-xs text-[var(--text-secondary)] font-mono">
                ₹{scanResult.summary.total_volume_dollars.toLocaleString()} total
              </span>
            </div>

            <div className="surface-card p-4 border border-[var(--color-safe-border)] bg-[var(--color-safe-bg)]">
              <span className="text-xs font-medium text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="h-3.5 w-3.5" />
                Approved
              </span>
              <p className="text-2xl font-bold font-mono text-emerald-300 mt-1">
                {scanResult.summary.approved_count}
              </p>
              <span className="text-xs text-emerald-400/80">Normal spending</span>
            </div>

            <div className="surface-card p-4 border border-[var(--color-warning-border)] bg-[var(--color-warning-bg)]">
              <span className="text-xs font-medium text-amber-400 flex items-center gap-1">
                <AlertTriangle className="h-3.5 w-3.5" />
                Suspicious
              </span>
              <p className="text-2xl font-bold font-mono text-amber-300 mt-1">
                {scanResult.summary.challenged_count}
              </p>
              <span className="text-xs text-amber-400/80">Requires verification</span>
            </div>

            <div className="surface-card p-4 border border-[var(--color-danger-border)] bg-[var(--color-danger-bg)]">
              <span className="text-xs font-medium text-rose-400 flex items-center gap-1">
                <ShieldAlert className="h-3.5 w-3.5" />
                Blocked
              </span>
              <p className="text-2xl font-bold font-mono text-rose-300 mt-1">
                {scanResult.summary.blocked_count}
              </p>
              <span className="text-xs text-rose-400/80 font-mono">
                ₹{scanResult.summary.flagged_volume_dollars.toLocaleString()} guarded
              </span>
            </div>

          </div>

          {/* Transaction Table */}
          <div className="surface-card border border-[var(--border-subtle)] overflow-hidden">
            <div className="px-5 py-3.5 border-b border-[var(--border-subtle)] flex items-center justify-between">
              <div>
                <h4 className="text-xs font-semibold text-white">
                  Transaction risk audit
                </h4>
                <p className="text-xs text-[var(--text-muted)]">
                  Evaluated with median cardholder baseline.
                </p>
              </div>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                scanResult.summary.account_health === "Healthy"
                  ? "bg-emerald-950/60 text-emerald-300 border-emerald-500/40"
                  : "bg-rose-950/60 text-rose-300 border-rose-500/40"
              }`}>
                Health: {scanResult.summary.account_health}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-[var(--bg-card-raised)] text-[var(--text-muted)] border-b border-[var(--border-subtle)]">
                    <th className="py-2.5 px-4 font-medium">Date</th>
                    <th className="py-2.5 px-4 font-medium">Description</th>
                    <th className="py-2.5 px-4 font-medium">Category</th>
                    <th className="py-2.5 px-4 font-medium text-right">Amount</th>
                    <th className="py-2.5 px-4 font-medium text-right">Threat %</th>
                    <th className="py-2.5 px-4 font-medium text-center">Status</th>
                    <th className="py-2.5 px-4 font-medium">Reason</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {scanResult.transactions.map((tx) => (
                    <tr key={tx.id} className="hover:bg-[var(--bg-card-raised)]/50 transition-colors">
                      <td className="py-2.5 px-4 text-[var(--text-muted)] font-mono whitespace-nowrap">{tx.date}</td>
                      <td className="py-2.5 px-4 font-medium text-white">{tx.description}</td>
                      <td className="py-2.5 px-4 text-[var(--text-secondary)] capitalize">{tx.category}</td>
                      <td className="py-2.5 px-4 text-right font-mono font-medium text-[var(--accent-light)]">₹{tx.amount.toFixed(2)}</td>
                      <td className="py-2.5 px-4 text-right font-mono font-semibold text-white">{tx.risk_score_percent}%</td>
                      <td className="py-2.5 px-4 text-center">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-semibold border ${
                          tx.status === "APPROVED"
                            ? "bg-emerald-950/60 text-emerald-300 border-emerald-500/40"
                            : tx.status === "CHALLENGE"
                            ? "bg-amber-950/60 text-amber-300 border-amber-500/40"
                            : "bg-rose-950/60 text-rose-300 border-rose-500/40"
                        }`}>
                          {tx.status}
                        </span>
                      </td>
                      <td className="py-2.5 px-4 text-[var(--text-secondary)] max-w-xs truncate">
                        {tx.top_reason}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      )}

      {/* Password Modal Dialog */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4">
          <div className="w-full max-w-md rounded-xl surface-card p-6 border border-[var(--border-strong)] shadow-xl relative">
            
            <div className={`h-11 w-11 rounded-lg flex items-center justify-center mx-auto mb-3 border ${
              modalType === "required"
                ? "bg-amber-950/60 border-amber-500/40 text-amber-400"
                : "bg-rose-950/60 border-rose-500/40 text-rose-400"
            }`}>
              {modalType === "required" ? (
                <KeyRound className="h-5 w-5" />
              ) : (
                <AlertTriangle className="h-5 w-5" />
              )}
            </div>

            <h3 className="text-base font-bold text-center text-white mb-1">
              {modalType === "required" ? "Password-protected statement" : "Incorrect statement password"}
            </h3>
            <p className="text-xs text-[var(--text-secondary)] text-center mb-4">
              {modalType === "required"
                ? "This statement is encrypted. Please enter your password or PIN to decrypt."
                : "The password entered could not unlock this statement. Please check and try again."}
            </p>

            {/* Bank Password Formats Tip */}
            <div className="mb-4 p-3 rounded-md bg-[var(--bg-canvas)] border border-[var(--border-subtle)] text-left">
              <p className="text-xs font-semibold text-[var(--accent-light)] mb-1">
                Common bank password formats:
              </p>
              <ul className="text-xs text-[var(--text-secondary)] space-y-0.5">
                <li>• SBI / HDFC: Date of Birth (DDMMYYYY) or registered mobile</li>
                <li>• ICICI / Axis: Registered mobile number or PAN (uppercase)</li>
                <li>• Kotak: CRN number or Date of Birth</li>
              </ul>
            </div>

            {/* Password Form */}
            <form onSubmit={handleModalSubmit} className="space-y-3">
              <div className="relative">
                <input
                  type={modalShowPwd ? "text" : "password"}
                  value={modalPwd}
                  onChange={(e) => setModalPwd(e.target.value)}
                  placeholder="Enter statement password"
                  autoFocus
                  className="w-full px-3 py-2 pr-10 text-xs rounded-md border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-white focus:border-[var(--accent-light)] focus:outline-hidden"
                />
                <button
                  type="button"
                  onClick={() => setModalShowPwd(!modalShowPwd)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-[var(--text-muted)] hover:text-white cursor-pointer"
                >
                  {modalShowPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-2 px-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-card-raised)] hover:bg-[var(--bg-card-subtle)] text-xs font-medium text-[var(--text-secondary)] transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 px-3 rounded-lg bg-[var(--accent-primary)] hover:bg-[var(--accent-hover)] text-xs font-semibold text-white transition-colors cursor-pointer"
                >
                  {modalType === "required" ? "Unlock & scan" : "Retry"}
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
}
