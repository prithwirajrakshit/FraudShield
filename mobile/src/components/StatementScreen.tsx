import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  TextInput,
  ActivityIndicator,
  Alert,
  Modal
} from "react-native";
import * as DocumentPicker from "expo-document-picker";
import * as Haptics from "expo-haptics";
import {
  FileText,
  Lock,
  Eye,
  EyeOff,
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  ShieldAlert,
  Terminal,
  IndianRupee,
  ShieldCheck,
  KeyRound,
  X,
  HelpCircle
} from "lucide-react-native";
import { uploadStatement, StatementScanResponse } from "../lib/api";
import { theme } from "../styles/theme";
import { GlowCard } from "./GlowCard";

export function StatementScreen() {
  const [selectedFile, setSelectedFile] = useState<{ uri: string; name: string; mimeType?: string } | null>(null);
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState<StatementScanResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [passwordErrorType, setPasswordErrorType] = useState<"required" | "incorrect" | null>(null);

  // Modal Dialog States
  const [pwdModalVisible, setPwdModalVisible] = useState(false);
  const [pwdModalType, setPwdModalType] = useState<"required" | "incorrect">("required");
  const [modalInputPwd, setModalInputPwd] = useState("");
  const [modalShowPwd, setModalShowPwd] = useState(false);

  const handlePickFile = async () => {
    try {
      Haptics.selectionAsync();
      const res = await DocumentPicker.getDocumentAsync({
        type: ["*/*"],
        copyToCacheDirectory: true,
      });

      if (!res.canceled && res.assets && res.assets.length > 0) {
        const file = res.assets[0];
        setSelectedFile({
          uri: file.uri,
          name: file.name,
          mimeType: file.mimeType,
        });
        setErrorMsg(null);
        setPasswordErrorType(null);
      }
    } catch (e: any) {
      Alert.alert("Picker Error", e.message || "Failed to pick file");
    }
  };

  const handleScan = async (overridePassword?: string) => {
    if (!selectedFile) {
      Alert.alert("No File Selected", "Please select a bank statement (.xlsx, .csv, .pdf, or .zip) first.");
      return;
    }

    const activePassword = overridePassword !== undefined ? overridePassword : password;

    try {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    } catch (e) {}

    setLoading(true);
    setErrorMsg(null);
    setPasswordErrorType(null);

    try {
      const res = await uploadStatement(selectedFile, activePassword);
      setScanResult(res);
      setPasswordErrorType(null);
      try {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      } catch (e) {}
    } catch (err: any) {
      const errType = err.errorType;
      const msg = err.message || "Failed to scan statement.";
      setErrorMsg(msg);

      try {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      } catch (e) {}

      // Trigger user-friendly popup modal
      if (errType === "PASSWORD_REQUIRED" || msg.toLowerCase().includes("password-protected") || msg.toLowerCase().includes("password required")) {
        setPasswordErrorType("required");
        setPwdModalType("required");
        setModalInputPwd("");
        setPwdModalVisible(true);
      } else if (errType === "PASSWORD_INCORRECT" || (msg.toLowerCase().includes("incorrect") && msg.toLowerCase().includes("password"))) {
        setPasswordErrorType("incorrect");
        setPwdModalType("incorrect");
        setModalInputPwd(activePassword);
        setPwdModalVisible(true);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleModalSubmit = () => {
    if (!modalInputPwd.trim()) {
      Alert.alert("Password Needed", "Please enter the password to unlock this statement.");
      return;
    }
    const cleanPwd = modalInputPwd.trim();
    setPassword(cleanPwd);
    setPwdModalVisible(false);
    handleScan(cleanPwd);
  };

  return (
    <View style={styles.rootWrapper}>
      <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer} showsVerticalScrollIndicator={false}>
      
      {/* Upload Box */}
      <GlowCard style={styles.uploadCard}>
        <View style={styles.headerRow}>
          <FileText size={18} color={theme.colors.cyan} />
          <Text style={styles.cardTitle}>Universal Bank Statement Scanner</Text>
        </View>
        <Text style={styles.cardSubtitle}>
          Select your bank statement in Excel (.xlsx), CSV, PDF, or ZIP. Works with all banks (SBI, HDFC, ICICI, Kotak, Axis, etc.).
        </Text>

        {/* File Selection Trigger */}
        <Pressable
          style={({ pressed }) => [styles.dropArea, pressed && { opacity: 0.85 }]}
          onPress={handlePickFile}
        >
          <UploadCloud size={32} color={selectedFile ? theme.colors.cyan : theme.colors.textSubtle} />
          {selectedFile ? (
            <View style={{ alignItems: "center", marginTop: 6 }}>
              <Text style={styles.fileName}>{selectedFile.name}</Text>
              <Text style={styles.fileChangeHint}>Tap to change statement</Text>
            </View>
          ) : (
            <View style={{ alignItems: "center", marginTop: 6 }}>
              <Text style={styles.dropText}>Tap to Browse Bank Statement</Text>
              <Text style={styles.dropSub}>Supported: XLSX, XLS, CSV, PDF, ZIP</Text>
            </View>
          )}
        </Pressable>

        {/* Password input (for protected statements) */}
        <View style={styles.passwordContainer}>
          <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <Text style={styles.passwordLabel}>Password / PIN (if statement is locked)</Text>
            {passwordErrorType && (
              <View style={[
                styles.pwdBadge, 
                passwordErrorType === "required" ? styles.pwdBadgeAmber : styles.pwdBadgeRose
              ]}>
                <Text style={[
                  styles.pwdBadgeText,
                  passwordErrorType === "required" ? { color: theme.colors.amberLight } : { color: theme.colors.roseLight }
                ]}>
                  {passwordErrorType === "required" ? "Password Required" : "Incorrect Password"}
                </Text>
              </View>
            )}
          </View>
          <View style={[
            styles.passwordInputRow,
            passwordErrorType === "required" && styles.inputBorderAmber,
            passwordErrorType === "incorrect" && styles.inputBorderRose
          ]}>
            <Lock size={16} color={passwordErrorType ? (passwordErrorType === "required" ? theme.colors.amber : theme.colors.rose) : theme.colors.textMuted} />
            <TextInput
              style={styles.passwordInput}
              value={password}
              onChangeText={(text) => {
                setPassword(text);
                if (passwordErrorType) setPasswordErrorType(null);
                if (errorMsg) setErrorMsg(null);
              }}
              placeholder="e.g. DOB (DDMMYYYY) or Mobile Number"
              placeholderTextColor={theme.colors.textSubtle}
              secureTextEntry={!showPassword}
              autoCapitalize="none"
            />
            <Pressable onPress={() => setShowPassword(!showPassword)} style={{ padding: 4 }}>
              {showPassword ? (
                <EyeOff size={16} color={theme.colors.textMuted} />
              ) : (
                <Eye size={16} color={theme.colors.textMuted} />
              )}
            </Pressable>
          </View>
        </View>

        {/* Error notification */}
        {errorMsg && (
          <View style={[
            styles.errorBox,
            passwordErrorType === "required" && { borderColor: theme.colors.amber, backgroundColor: "rgba(120, 53, 15, 0.3)" }
          ]}>
            <AlertTriangle size={16} color={passwordErrorType === "required" ? theme.colors.amber : theme.colors.rose} />
            <Text style={[
              styles.errorText,
              passwordErrorType === "required" && { color: theme.colors.amberLight }
            ]}>
              {errorMsg}
            </Text>
          </View>
        )}

        {/* Scan Button */}
        <Pressable
          style={({ pressed }) => [
            styles.scanBtn,
            (!selectedFile || loading) && styles.scanBtnDisabled,
            pressed && { opacity: 0.85 }
          ]}
          onPress={() => handleScan()}
          disabled={!selectedFile || loading}
        >
          {loading ? (
            <ActivityIndicator color="#030712" />
          ) : (
            <>
              <ShieldCheck size={18} color="#030712" strokeWidth={2.5} />
              <Text style={styles.scanBtnText}>Scan Statement for Fraud Anomaly</Text>
            </>
          )}
        </Pressable>
      </GlowCard>

      {/* Telemetry Results Section */}
      {scanResult && (
        <View style={styles.resultsSection}>
          
          {/* KPI Grid */}
          <View style={styles.kpiGrid}>
            
            <GlowCard style={styles.kpiCard}>
              <Text style={styles.kpiLabel}>Scanned Volume</Text>
              <Text style={styles.kpiVal}>{scanResult.summary.total_transactions}</Text>
              <Text style={styles.kpiSub}>₹{scanResult.summary.total_volume_dollars.toLocaleString()}</Text>
            </GlowCard>

            <GlowCard style={[styles.kpiCard, { borderColor: "rgba(16, 185, 129, 0.4)" }]}>
              <View style={{ flexDirection: "row", alignItems: "center", gap: 4 }}>
                <CheckCircle2 size={11} color={theme.colors.emerald} />
                <Text style={[styles.kpiLabel, { color: theme.colors.emerald }]}>Approved</Text>
              </View>
              <Text style={[styles.kpiVal, { color: theme.colors.emeraldLight }]}>{scanResult.summary.approved_count}</Text>
              <Text style={styles.kpiSub}>Cleared Safe</Text>
            </GlowCard>

            <GlowCard style={[styles.kpiCard, { borderColor: "rgba(245, 158, 11, 0.4)" }]}>
              <View style={{ flexDirection: "row", alignItems: "center", gap: 4 }}>
                <AlertTriangle size={11} color={theme.colors.amber} />
                <Text style={[styles.kpiLabel, { color: theme.colors.amber }]}>Challenged</Text>
              </View>
              <Text style={[styles.kpiVal, { color: theme.colors.amberLight }]}>{scanResult.summary.challenged_count}</Text>
              <Text style={styles.kpiSub}>OTP 2FA</Text>
            </GlowCard>

            <GlowCard style={[styles.kpiCard, { borderColor: "rgba(244, 63, 94, 0.4)" }]}>
              <View style={{ flexDirection: "row", alignItems: "center", gap: 4 }}>
                <ShieldAlert size={11} color={theme.colors.rose} />
                <Text style={[styles.kpiLabel, { color: theme.colors.rose }]}>Blocked</Text>
              </View>
              <Text style={[styles.kpiVal, { color: theme.colors.roseLight }]}>{scanResult.summary.blocked_count}</Text>
              <Text style={styles.kpiSub}>₹{scanResult.summary.flagged_volume_dollars.toLocaleString()}</Text>
            </GlowCard>

          </View>

          {/* Account Health Banner */}
          <View style={[
            styles.healthBanner, 
            scanResult.summary.account_health === "Healthy" 
              ? styles.healthBannerSafe 
              : styles.healthBannerAlert
          ]}>
            <Text style={styles.healthTitle}>
              Security Health: {scanResult.summary.account_health}
            </Text>
            <Text style={styles.healthSub}>
              {scanResult.summary.account_health === "Healthy"
                ? "No high-entropy breach signals found."
                : "Transactions flagged with elevated threat vectors."}
            </Text>
          </View>

          {/* Telemetry Transaction Feed */}
          <View style={styles.feedHeader}>
            <Terminal size={14} color={theme.colors.cyan} />
            <Text style={styles.feedTitle}>Transaction Audit Feed ({scanResult.transactions.length})</Text>
          </View>

          {scanResult.transactions.map((tx) => {
            const isApproved = tx.status === "APPROVED";
            const isChallenge = tx.status === "CHALLENGE";

            return (
              <GlowCard key={tx.id} style={styles.txCard}>
                <View style={styles.txTopRow}>
                  <Text style={styles.txDate}>{tx.date}</Text>
                  <View style={[
                    styles.txStatusBadge,
                    isApproved ? styles.badgeApproved : (isChallenge ? styles.badgeChallenge : styles.badgeBlocked)
                  ]}>
                    <Text style={[
                      styles.txStatusText,
                      isApproved ? { color: theme.colors.emeraldLight } : (isChallenge ? { color: theme.colors.amberLight } : { color: theme.colors.roseLight })
                    ]}>
                      {tx.status} • {tx.risk_score_percent}%
                    </Text>
                  </View>
                </View>

                <Text style={styles.txDesc} numberOfLines={2}>{tx.description}</Text>

                <View style={styles.txBottomRow}>
                  <Text style={styles.txAmt}>₹{tx.amount.toFixed(2)}</Text>
                  <Text style={styles.txReason} numberOfLines={1}>{tx.top_reason}</Text>
                </View>
              </GlowCard>
            );
          })}

        </View>
      )}

      </ScrollView>

      {/* Password Prompt & Error Modal Dialog */}
      <Modal
        visible={pwdModalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setPwdModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            
            {/* Modal Icon Badge */}
            <View style={[
              styles.modalIconBadge,
              pwdModalType === "required" ? styles.modalIconBadgeAmber : styles.modalIconBadgeRose
            ]}>
              {pwdModalType === "required" ? (
                <KeyRound size={26} color={theme.colors.amber} strokeWidth={2.2} />
              ) : (
                <AlertTriangle size={26} color={theme.colors.rose} strokeWidth={2.2} />
              )}
            </View>

            {/* Modal Title */}
            <Text style={styles.modalTitle}>
              {pwdModalType === "required" ? "Password-Protected Statement" : "Incorrect Statement Password"}
            </Text>

            {/* Modal Subtitle / Explainer */}
            <Text style={styles.modalSub}>
              {pwdModalType === "required"
                ? "This bank statement is encrypted with a password. Please enter your password or PIN below to decrypt and scan."
                : "The password entered could not unlock this statement. Please verify your bank's format and try again."}
            </Text>

            {/* Bank Password Format Hints */}
            <View style={styles.bankHintsCard}>
              <Text style={styles.hintsTitle}>💡 Common Bank Password Formats:</Text>
              <Text style={styles.hintsText}>• <Text style={styles.hintBank}>SBI / HDFC:</Text> Date of Birth (DDMMYYYY) or Mobile Number</Text>
              <Text style={styles.hintsText}>• <Text style={styles.hintBank}>ICICI / Axis:</Text> Registered Mobile Number or PAN in UPPERCASE</Text>
              <Text style={styles.hintsText}>• <Text style={styles.hintBank}>Kotak:</Text> CRN or Date of Birth (DDMMYYYY)</Text>
            </View>

            {/* Password Input Row inside Modal */}
            <View style={styles.modalInputRow}>
              <Lock size={16} color={theme.colors.textMuted} />
              <TextInput
                style={styles.modalInput}
                value={modalInputPwd}
                onChangeText={setModalInputPwd}
                placeholder="Enter Statement Password"
                placeholderTextColor={theme.colors.textSubtle}
                secureTextEntry={!modalShowPwd}
                autoFocus={true}
                autoCapitalize="none"
              />
              <Pressable onPress={() => setModalShowPwd(!modalShowPwd)} style={{ padding: 4 }}>
                {modalShowPwd ? (
                  <EyeOff size={16} color={theme.colors.textMuted} />
                ) : (
                  <Eye size={16} color={theme.colors.textMuted} />
                )}
              </Pressable>
            </View>

            {/* Modal Buttons */}
            <View style={styles.modalBtnRow}>
              <Pressable 
                style={styles.modalCancelBtn} 
                onPress={() => setPwdModalVisible(false)}
              >
                <Text style={styles.modalCancelBtnText}>Cancel</Text>
              </Pressable>

              <Pressable 
                style={[
                  styles.modalSubmitBtn,
                  pwdModalType === "required" ? styles.modalSubmitBtnAmber : styles.modalSubmitBtnCyan
                ]} 
                onPress={handleModalSubmit}
              >
                <ShieldCheck size={16} color="#030712" strokeWidth={2.5} />
                <Text style={styles.modalSubmitBtnText}>
                  {pwdModalType === "required" ? "Unlock & Scan" : "Try Again"}
                </Text>
              </Pressable>
            </View>

          </View>
        </View>
      </Modal>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.bg,
  },
  contentContainer: {
    padding: 16,
    paddingBottom: 40,
  },
  uploadCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 18,
    marginBottom: 16,
  },
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 6,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: "800",
    color: "#ffffff",
  },
  cardSubtitle: {
    fontSize: 11,
    color: theme.colors.textMuted,
    lineHeight: 16,
    marginBottom: 14,
  },
  dropArea: {
    borderWidth: 1.5,
    borderStyle: "dashed",
    borderColor: "rgba(6, 182, 212, 0.4)",
    backgroundColor: "rgba(3, 7, 18, 0.7)",
    borderRadius: 16,
    padding: 24,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 14,
  },
  fileName: {
    fontSize: 13,
    fontWeight: "800",
    color: theme.colors.cyanLight,
    textAlign: "center",
  },
  fileChangeHint: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    marginTop: 2,
  },
  dropText: {
    fontSize: 13,
    fontWeight: "700",
    color: "#ffffff",
  },
  dropSub: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    marginTop: 2,
  },
  passwordContainer: {
    marginBottom: 14,
  },
  passwordLabel: {
    fontSize: 10,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginBottom: 6,
  },
  passwordInputRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#030712",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    paddingHorizontal: 12,
    height: 44,
  },
  passwordInput: {
    flex: 1,
    color: "#ffffff",
    fontSize: 13,
    marginLeft: 8,
  },
  errorBox: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    backgroundColor: "rgba(136, 19, 55, 0.3)",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.rose,
    padding: 10,
    marginBottom: 14,
  },
  errorText: {
    flex: 1,
    fontSize: 11,
    color: theme.colors.roseLight,
    fontWeight: "600",
  },
  scanBtn: {
    backgroundColor: theme.colors.cyan,
    borderRadius: 14,
    paddingVertical: 14,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  },
  scanBtnDisabled: {
    opacity: 0.45,
  },
  scanBtnText: {
    fontSize: 13,
    fontWeight: "900",
    color: "#030712",
    textTransform: "uppercase",
  },
  resultsSection: {
    marginTop: 6,
  },
  kpiGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
    marginBottom: 12,
  },
  kpiCard: {
    flex: 1,
    minWidth: "47%",
    backgroundColor: theme.colors.surface,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 12,
  },
  kpiLabel: {
    fontSize: 10,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  kpiVal: {
    fontSize: 22,
    fontWeight: "900",
    color: "#ffffff",
    marginVertical: 2,
  },
  kpiSub: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    fontWeight: "600",
  },
  healthBanner: {
    padding: 12,
    borderRadius: 14,
    borderWidth: 1,
    marginBottom: 16,
  },
  healthBannerSafe: {
    backgroundColor: "rgba(6, 78, 59, 0.3)",
    borderColor: theme.colors.emerald,
  },
  healthBannerAlert: {
    backgroundColor: "rgba(136, 19, 55, 0.3)",
    borderColor: theme.colors.rose,
  },
  healthTitle: {
    fontSize: 12,
    fontWeight: "800",
    color: "#ffffff",
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  healthSub: {
    fontSize: 10,
    color: theme.colors.textMuted,
    marginTop: 2,
  },
  feedHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 10,
  },
  feedTitle: {
    fontSize: 11,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  txCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 12,
    marginBottom: 8,
  },
  txTopRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  txDate: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    fontWeight: "600",
  },
  txStatusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
    borderWidth: 1,
  },
  badgeApproved: {
    backgroundColor: "rgba(6, 78, 59, 0.6)",
    borderColor: theme.colors.emerald,
  },
  badgeChallenge: {
    backgroundColor: "rgba(120, 53, 15, 0.6)",
    borderColor: theme.colors.amber,
  },
  badgeBlocked: {
    backgroundColor: "rgba(136, 19, 55, 0.6)",
    borderColor: theme.colors.rose,
  },
  txStatusText: {
    fontSize: 9,
    fontWeight: "800",
    textTransform: "uppercase",
  },
  txDesc: {
    fontSize: 12,
    fontWeight: "700",
    color: "#ffffff",
    marginBottom: 6,
  },
  txBottomRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  txAmt: {
    fontSize: 13,
    fontWeight: "900",
    color: theme.colors.cyanLight,
  },
  txReason: {
    fontSize: 10,
    color: theme.colors.textMuted,
    maxWidth: "60%",
  },
  rootWrapper: {
    flex: 1,
    backgroundColor: theme.colors.bg,
  },
  pwdBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    borderWidth: 1,
  },
  pwdBadgeAmber: {
    backgroundColor: "rgba(120, 53, 15, 0.4)",
    borderColor: theme.colors.amber,
  },
  pwdBadgeRose: {
    backgroundColor: "rgba(136, 19, 55, 0.4)",
    borderColor: theme.colors.rose,
  },
  pwdBadgeText: {
    fontSize: 9,
    fontWeight: "800",
    textTransform: "uppercase",
  },
  inputBorderAmber: {
    borderColor: theme.colors.amber,
    backgroundColor: "rgba(120, 53, 15, 0.15)",
  },
  inputBorderRose: {
    borderColor: theme.colors.rose,
    backgroundColor: "rgba(136, 19, 55, 0.15)",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(3, 7, 18, 0.85)",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  modalContent: {
    width: "100%",
    maxWidth: 380,
    backgroundColor: theme.colors.surface,
    borderRadius: 22,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 22,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 10,
  },
  modalIconBadge: {
    width: 54,
    height: 54,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 14,
    borderWidth: 1,
  },
  modalIconBadgeAmber: {
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    borderColor: "rgba(245, 158, 11, 0.4)",
  },
  modalIconBadgeRose: {
    backgroundColor: "rgba(244, 63, 94, 0.15)",
    borderColor: "rgba(244, 63, 94, 0.4)",
  },
  modalTitle: {
    fontSize: 16,
    fontWeight: "900",
    color: "#ffffff",
    textAlign: "center",
    marginBottom: 6,
  },
  modalSub: {
    fontSize: 12,
    color: theme.colors.textMuted,
    textAlign: "center",
    lineHeight: 18,
    marginBottom: 14,
  },
  bankHintsCard: {
    width: "100%",
    backgroundColor: "rgba(3, 7, 18, 0.6)",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.08)",
    padding: 10,
    marginBottom: 16,
  },
  hintsTitle: {
    fontSize: 11,
    fontWeight: "800",
    color: theme.colors.cyanLight,
    marginBottom: 4,
  },
  hintsText: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    lineHeight: 15,
  },
  hintBank: {
    color: theme.colors.textMuted,
    fontWeight: "700",
  },
  modalInputRow: {
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#030712",
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: theme.colors.cyan,
    paddingHorizontal: 12,
    height: 48,
    marginBottom: 18,
  },
  modalInput: {
    flex: 1,
    color: "#ffffff",
    fontSize: 14,
    marginLeft: 8,
    fontWeight: "600",
  },
  modalBtnRow: {
    width: "100%",
    flexDirection: "row",
    gap: 10,
  },
  modalCancelBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    alignItems: "center",
    justifyContent: "center",
  },
  modalCancelBtnText: {
    fontSize: 12,
    fontWeight: "700",
    color: theme.colors.textMuted,
  },
  modalSubmitBtn: {
    flex: 2,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    paddingVertical: 12,
    borderRadius: 12,
  },
  modalSubmitBtnAmber: {
    backgroundColor: theme.colors.amber,
  },
  modalSubmitBtnCyan: {
    backgroundColor: theme.colors.cyan,
  },
  modalSubmitBtnText: {
    fontSize: 12,
    fontWeight: "900",
    color: "#030712",
    textTransform: "uppercase",
  },
});

