import React, { useState } from "react";
import { View, Text, StyleSheet, Modal, TextInput, Pressable, ActivityIndicator } from "react-native";
import { Server, CheckCircle2, XCircle, X, Globe, Wifi } from "lucide-react-native";
import { getApiBase, setApiBase, checkHealth } from "../lib/api";
import { theme } from "../styles/theme";

interface ServerConfigModalProps {
  visible: boolean;
  onClose: () => void;
  onServerUpdated: (status: "online" | "offline") => void;
}

export function ServerConfigModal({ visible, onClose, onServerUpdated }: ServerConfigModalProps) {
  const [url, setUrl] = useState(getApiBase());
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ status: string; engine?: string } | null>(null);

  const presets = [
    { label: "Detected Host Wi-Fi", url: "http://10.189.141.31:8000" },
    { label: "Android Emulator", url: "http://10.0.2.2:8000" },
    { label: "Localhost", url: "http://127.0.0.1:8000" },
  ];

  const handleTest = async (testUrl?: string) => {
    const target = testUrl || url;
    setTesting(true);
    setTestResult(null);
    setApiBase(target);

    try {
      const res = await checkHealth();
      setTestResult(res);
      onServerUpdated(res.status === "healthy" ? "online" : "offline");
    } catch (e) {
      setTestResult({ status: "offline" });
      onServerUpdated("offline");
    } finally {
      setTesting(false);
    }
  };

  const handleSaveAndClose = () => {
    setApiBase(url);
    onClose();
  };

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <View style={styles.overlay}>
        <View style={styles.modalCard}>
          
          <View style={styles.header}>
            <View style={styles.titleRow}>
              <Server size={18} color={theme.colors.cyan} />
              <Text style={styles.title}>FastAPI Backend Link</Text>
            </View>
            <Pressable onPress={onClose} style={styles.closeBtn}>
              <X size={18} color={theme.colors.textMuted} />
            </Pressable>
          </View>

          <Text style={styles.subtitle}>
            Enter the IP & Port of your running FastAPI AI server. For physical phones, use your computer's Wi-Fi LAN IP.
          </Text>

          {/* Presets */}
          <View style={styles.presetsRow}>
            {presets.map((p) => (
              <Pressable
                key={p.url}
                style={[styles.presetChip, url === p.url && styles.presetChipActive]}
                onPress={() => {
                  setUrl(p.url);
                  handleTest(p.url);
                }}
              >
                <Text style={[styles.presetChipText, url === p.url && styles.presetChipTextActive]}>
                  {p.label}
                </Text>
              </Pressable>
            ))}
          </View>

          {/* URL Input */}
          <View style={styles.inputContainer}>
            <Globe size={16} color={theme.colors.textMuted} style={styles.inputIcon} />
            <TextInput
              style={styles.input}
              value={url}
              onChangeText={setUrl}
              placeholder="http://192.168.1.15:8000"
              placeholderTextColor={theme.colors.textSubtle}
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>

          {/* Test Status Indicator */}
          {testing && (
            <View style={styles.statusBox}>
              <ActivityIndicator size="small" color={theme.colors.cyan} />
              <Text style={styles.statusBoxText}>Testing connection to {url}...</Text>
            </View>
          )}

          {testResult && (
            <View style={[
              styles.statusBox, 
              testResult.status === "healthy" ? styles.statusBoxSuccess : styles.statusBoxError
            ]}>
              {testResult.status === "healthy" ? (
                <>
                  <CheckCircle2 size={16} color={theme.colors.emerald} />
                  <View style={{ flex: 1 }}>
                    <Text style={styles.statusSuccessTitle}>AI Backend Connected</Text>
                    <Text style={styles.statusSuccessDesc}>{testResult.engine || "PyTorch Focal Loss Engine"}</Text>
                  </View>
                </>
              ) : (
                <>
                  <XCircle size={16} color={theme.colors.rose} />
                  <View style={{ flex: 1 }}>
                    <Text style={styles.statusErrorTitle}>Backend Offline</Text>
                    <Text style={styles.statusErrorDesc}>Verify server is running with --host 0.0.0.0 or 127.0.0.1.</Text>
                  </View>
                </>
              )}
            </View>
          )}

          {/* Actions */}
          <View style={styles.actionRow}>
            <Pressable style={styles.testBtn} onPress={() => handleTest()}>
              <Text style={styles.testBtnText}>Test Ping</Text>
            </Pressable>
            <Pressable style={styles.saveBtn} onPress={handleSaveAndClose}>
              <Text style={styles.saveBtnText}>Save & Apply</Text>
            </Pressable>
          </View>

        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(3, 7, 18, 0.85)",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  modalCard: {
    width: "100%",
    backgroundColor: theme.colors.surface,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 20,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  title: {
    fontSize: 16,
    fontWeight: "800",
    color: "#ffffff",
  },
  closeBtn: {
    padding: 4,
  },
  subtitle: {
    fontSize: 12,
    color: theme.colors.textMuted,
    lineHeight: 18,
    marginBottom: 14,
  },
  presetsRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
    marginBottom: 12,
  },
  presetChip: {
    backgroundColor: "#0f172a",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  presetChipActive: {
    backgroundColor: "rgba(6, 182, 212, 0.15)",
    borderColor: theme.colors.cyan,
  },
  presetChipText: {
    fontSize: 11,
    color: theme.colors.textMuted,
    fontWeight: "600",
  },
  presetChipTextActive: {
    color: theme.colors.cyanLight,
    fontWeight: "800",
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#030712",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    paddingHorizontal: 12,
    marginBottom: 12,
  },
  inputIcon: {
    marginRight: 8,
  },
  input: {
    flex: 1,
    height: 44,
    color: "#ffffff",
    fontSize: 13,
    fontFamily: theme.fonts.mono,
  },
  statusBox: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    backgroundColor: "#0f172a",
    padding: 10,
    borderRadius: 12,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  statusBoxSuccess: {
    backgroundColor: "rgba(6, 78, 59, 0.3)",
    borderColor: theme.colors.emerald,
  },
  statusBoxError: {
    backgroundColor: "rgba(136, 19, 55, 0.3)",
    borderColor: theme.colors.rose,
  },
  statusBoxText: {
    fontSize: 12,
    color: theme.colors.textMuted,
  },
  statusSuccessTitle: {
    fontSize: 12,
    fontWeight: "800",
    color: theme.colors.emeraldLight,
  },
  statusSuccessDesc: {
    fontSize: 10,
    color: theme.colors.textMuted,
  },
  statusErrorTitle: {
    fontSize: 12,
    fontWeight: "800",
    color: theme.colors.roseLight,
  },
  statusErrorDesc: {
    fontSize: 10,
    color: theme.colors.textMuted,
  },
  actionRow: {
    flexDirection: "row",
    gap: 10,
  },
  testBtn: {
    flex: 1,
    backgroundColor: "#1e293b",
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
  },
  testBtnText: {
    color: theme.colors.text,
    fontSize: 13,
    fontWeight: "700",
  },
  saveBtn: {
    flex: 1,
    backgroundColor: theme.colors.cyan,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
  },
  saveBtnText: {
    color: "#030712",
    fontSize: 13,
    fontWeight: "800",
  },
});

