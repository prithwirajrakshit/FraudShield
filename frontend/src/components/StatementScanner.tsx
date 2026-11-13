"use client";

import React, { useState } from "react";
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, ShieldAlert, Sparkles, RefreshCw, Terminal, ScanLine, Lock, Eye, EyeOff, KeyRound } from "lucide-react";
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
      
      {/* Upload Zone with Laser Scanning Aesthetic */}
      <div className="relative overflow-hidden rounded-2xl border-2 border-dashed border-slate-700/80 hover:border-cyan-500/80 glass-panel p-8 text-center transition-all duration-300">
        
        {/* Animated Laser Beam when Scanning */}
        {isLoading && (
          <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-lg shadow-cyan-400/80 laser-beam z-20"></div>
        )}

        <div className="relative z-10 max-w-xl mx-auto">
          <div className="h-14 w-14 rounded-2xl bg-cyan-950/70 border border-cyan-800/80 flex items-center justify-center text-cyan-400 mx-auto mb-3 shadow-lg shadow-cyan-950/40">
            <ScanLine className="h-7 w-7 text-cyan-400" />
          </div>

          <h3 className="text-lg font-mono font-bold tracking-tight text-white">
            Bank Statement Security Scanner
          </h3>
          <p className="text-xs text-slate-400 mt-1 mb-5 leading-relaxed">
            Upload your 1-month bank statement (supports <b>.CSV</b>, <b>.ZIP</b>, <b>.XLSX</b>, and <b>.PDF</b>). Supports password-protected statements.
          </p>

          {/* Optional Password Input Field for Protected Statements */}
          <div className={`mb-5 p-4 rounded-xl border text-left transition-all ${
            passwordErrorType === "required"
              ? "border-amber-500/80 bg-amber-950/20 shadow-lg shadow-amber-950/30"
              : passwordErrorType === "incorrect"
              ? "border-rose-500/80 bg-rose-950/20 shadow-lg shadow-rose-950/30"
              : "border-slate-800 bg-slate-950/80"
          }`}>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-mono font-bold text-slate-300 flex items-center gap-1.5">
                <Lock className={`h-3.5 w-3.5 ${
                  passwordErrorType === "required" ? "text-amber-400" : passwordErrorType === "incorrect" ? "text-rose-400" : "text-cyan-400"
                }`} />
                <span>Statement Password (If Protected)</span>
              </label>
              {passwordErrorType ? (
                <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold border ${
                  passwordErrorType === "required"
                    ? "bg-amber-950 text-amber-300 border-amber-600/50"
                    : "bg-rose-950 text-rose-300 border-rose-600/50"
                }`}>
                  {passwordErrorType === "required" ? "Password Required" : "Incorrect Password"}
                </span>
              ) : (
                <span className="text-[10px] font-mono text-slate-500 uppercase">Optional</span>
              )}
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
                placeholder="Enter password (e.g., DOB: DDMMYYYY, PAN, or Mobile No)"
                className={`w-full px-3.5 py-2.5 pr-10 text-xs font-mono rounded-lg border bg-slate-900 text-white placeholder-slate-500 focus:outline-hidden ${
                  passwordErrorType === "required"
                    ? "border-amber-500 ring-1 ring-amber-500/30"
                    : passwordErrorType === "incorrect"
                    ? "border-rose-500 ring-1 ring-rose-500/30"
                    : "border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/20"
                }`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            <p className="text-[10px] text-slate-500 mt-1.5 font-mono">
              🔒 Decryption runs 100% in-memory. Passwords and statement data are never saved to disk.
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <label className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-mono font-bold text-xs uppercase tracking-wider shadow-lg shadow-cyan-500/25 border border-cyan-400/40 cursor-pointer transition-all">
              Choose Statement File
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
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 hover:border-cyan-500/50 text-slate-200 font-mono font-semibold text-xs tracking-wider transition-all cursor-pointer shadow-xs"
            >
              <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
              <span>Load Preset Demo</span>
            </button>
          </div>

          {file && (
            <div className="mt-4 inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs font-mono text-cyan-300">
              <FileText className="h-4 w-4 text-cyan-400" />
              <span>{file.name}</span>
              <button
                onClick={() => runScan(file)}
                disabled={isLoading}
                className="ml-2 font-bold text-white hover:text-cyan-300 underline cursor-pointer"
              >
                {isLoading ? "Decrypting & Scanning..." : "Unlock & Scan Now"}
              </button>
            </div>
          )}

          {error && (
            <div className="mt-4 p-3 rounded-xl border border-rose-500/40 bg-rose-950/40 text-xs font-mono text-rose-300 flex items-start gap-2.5 text-left">
              <KeyRound className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Authentication / File Notice:</p>
                <p className="text-rose-200 mt-0.5">{error}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Loading Readout */}
      {isLoading && (
        <div className="py-10 text-center space-y-3 glass-panel rounded-2xl border border-slate-800">
          <RefreshCw className="h-7 w-7 text-cyan-400 animate-spin mx-auto" />
          <p className="text-xs font-mono text-cyan-300 uppercase tracking-widest">
            Decrypting & Scanning Transaction Embeddings Through Deep Focal Network...
          </p>
        </div>
      )}

      {/* Results View */}
      {scanResult && !isLoading && (
        <div className="space-y-6">
          
          {/* Summary Telemetry Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            
            <div className="p-4 rounded-xl border border-slate-800 bg-slate-950/80 glass-panel">
              <span className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-widest">
                Scanned Volume
              </span>
              <p className="text-2xl font-black font-mono text-white mt-1">
                {scanResult.summary.total_transactions}
              </p>
              <span className="text-xs font-mono text-slate-400">
                ₹{scanResult.summary.total_volume_dollars.toLocaleString()} total
              </span>
            </div>

            <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-950/30 glass-panel">
              <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase tracking-widest flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3" />
                Approved
              </span>
              <p className="text-2xl font-black font-mono text-emerald-300 mt-1">
                {scanResult.summary.approved_count}
              </p>
              <span className="text-xs font-mono text-emerald-400/80">Cleared Safe</span>
            </div>

            <div className="p-4 rounded-xl border border-amber-500/30 bg-amber-950/30 glass-panel">
              <span className="text-[10px] font-mono font-bold text-amber-400 uppercase tracking-widest flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                Suspicious
              </span>
              <p className="text-2xl font-black font-mono text-amber-300 mt-1">
                {scanResult.summary.challenged_count}
              </p>
              <span className="text-xs font-mono text-amber-400/80">OTP Challenge</span>
            </div>

            <div className="p-4 rounded-xl border border-rose-500/40 bg-rose-950/30 glass-panel">
              <span className="text-[10px] font-mono font-bold text-rose-400 uppercase tracking-widest flex items-center gap-1">
                <ShieldAlert className="h-3 w-3" />
                Blocked
              </span>
              <p className="text-2xl font-black font-mono text-rose-300 mt-1">
                {scanResult.summary.blocked_count}
              </p>
              <span className="text-xs font-mono text-rose-400/80">
                ₹{scanResult.summary.flagged_volume_dollars.toLocaleString()} Protected
              </span>
            </div>

          </div>

          {/* Futuristic Data Breakdown Table */}
          <div className="rounded-2xl border border-slate-800 glass-panel overflow-hidden shadow-2xl">
            <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                  <Terminal className="h-4 w-4" />
                  <span>Telemetry Audit Feed</span>
                </h4>
                <p className="text-xs text-slate-400">
                  Individual anomaly calculations based on consumer spending profiles.
                </p>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider ${
                scanResult.summary.account_health === "Healthy"
                  ? "bg-emerald-950 text-emerald-300 border border-emerald-500/50"
                  : "bg-rose-950 text-rose-300 border border-rose-500/50"
              }`}>
                Security Health: {scanResult.summary.account_health}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse font-mono text-xs">
                <thead>
                  <tr className="bg-slate-900/90 text-slate-400 uppercase tracking-widest text-[10px] border-b border-slate-800">
                    <th className="py-3 px-4">Date</th>
                    <th className="py-3 px-4">Merchant Entity</th>
                    <th className="py-3 px-4">Sector</th>
                    <th className="py-3 px-4">Amount</th>
                    <th className="py-3 px-4">Threat %</th>
                    <th className="py-3 px-4">Decision</th>
                    <th className="py-3 px-4">Key Anomaly Signal</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {scanResult.transactions.map((tx) => (
                    <tr key={tx.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-3 px-4 text-slate-400 whitespace-nowrap">{tx.date}</td>
                      <td className="py-3 px-4 font-bold text-white">{tx.description}</td>
                      <td className="py-3 px-4 text-slate-300 capitalize">{tx.category}</td>
                      <td className="py-3 px-4 font-bold text-cyan-300">₹{tx.amount.toFixed(2)}</td>
                      <td className="py-3 px-4 font-black text-white">{tx.risk_score_percent}%</td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
                          tx.status === "APPROVED"
                            ? "bg-emerald-950/80 text-emerald-300 border-emerald-500/50"
                            : tx.status === "CHALLENGE"
                            ? "bg-amber-950/80 text-amber-300 border-amber-500/50"
                            : "bg-rose-950/90 text-rose-300 border-rose-500/60"
                        }`}>
                          {tx.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-300 max-w-xs truncate">
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

      {/* Password Prompt & Error Modal Dialog for Web */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 animate-in fade-in duration-200">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl shadow-cyan-950/40 relative">
            
            {/* Modal Icon Badge */}
            <div className={`h-14 w-14 rounded-2xl flex items-center justify-center mx-auto mb-4 border ${
              modalType === "required"
                ? "bg-amber-950/70 border-amber-500/50 text-amber-400 shadow-lg shadow-amber-950/40"
                : "bg-rose-950/70 border-rose-500/50 text-rose-400 shadow-lg shadow-rose-950/40"
            }`}>
              {modalType === "required" ? (
                <KeyRound className="h-7 w-7 text-amber-400" />
              ) : (
                <AlertTriangle className="h-7 w-7 text-rose-400" />
              )}
            </div>

            {/* Modal Header */}
            <h3 className="text-lg font-mono font-bold text-center text-white mb-2">
              {modalType === "required" ? "Password-Protected Statement" : "Incorrect Statement Password"}
            </h3>
            <p className="text-xs text-slate-400 text-center leading-relaxed mb-4">
              {modalType === "required"
                ? "This bank statement is encrypted with a password. Please enter your password or PIN below to decrypt and scan."
                : "The password entered could not unlock this statement. Please verify your bank's format and re-enter."}
            </p>

            {/* Common Bank Password Formats Tip */}
            <div className="mb-4 p-3 rounded-xl bg-slate-950 border border-slate-800 text-left">
              <p className="text-[11px] font-mono font-bold text-cyan-400 mb-1">
                💡 Common Bank Password Formats:
              </p>
              <ul className="text-[10px] text-slate-400 space-y-1 font-mono">
                <li>• <span className="text-slate-300 font-bold">SBI / HDFC:</span> Date of Birth (DDMMYYYY) or Mobile Number</li>
                <li>• <span className="text-slate-300 font-bold">ICICI / Axis:</span> Registered Mobile Number or PAN in UPPERCASE</li>
                <li>• <span className="text-slate-300 font-bold">Kotak:</span> CRN Number or Date of Birth (DDMMYYYY)</li>
              </ul>
            </div>

            {/* Password Input Form */}
            <form onSubmit={handleModalSubmit} className="space-y-4">
              <div className="relative">
                <input
                  type={modalShowPwd ? "text" : "password"}
                  value={modalPwd}
                  onChange={(e) => setModalPwd(e.target.value)}
                  placeholder="Enter Statement Password"
                  autoFocus
                  className="w-full px-3.5 py-2.5 pr-10 text-xs font-mono rounded-lg border border-cyan-500/80 bg-slate-950 text-white placeholder-slate-500 focus:ring-1 focus:ring-cyan-500/40 focus:outline-hidden"
                />
                <button
                  type="button"
                  onClick={() => setModalShowPwd(!modalShowPwd)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-200 cursor-pointer"
                >
                  {modalShowPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>

              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-2.5 px-4 rounded-xl border border-slate-700 bg-slate-800/60 hover:bg-slate-800 text-xs font-mono font-bold text-slate-300 transition-all cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className={`flex-2 py-2.5 px-4 rounded-xl text-xs font-mono font-bold text-slate-950 uppercase tracking-wider transition-all cursor-pointer ${
                    modalType === "required"
                      ? "bg-amber-400 hover:bg-amber-300 shadow-lg shadow-amber-500/20"
                      : "bg-cyan-400 hover:bg-cyan-300 shadow-lg shadow-cyan-500/20"
                  }`}
                >
                  {modalType === "required" ? "Unlock & Scan" : "Try Again"}
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
}
