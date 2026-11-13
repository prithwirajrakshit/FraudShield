import React from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { ShieldCheck, Settings, Server } from "lucide-react-native";
import { theme } from "../styles/theme";

interface NavbarProps {
  onOpenSettings: () => void;
  serverStatus: "online" | "offline" | "checking";
}

export function Navbar({ onOpenSettings, serverStatus }: NavbarProps) {
  return (
    <View style={styles.container}>
      <View style={styles.brandRow}>
        <View style={styles.logoBadge}>
          <ShieldCheck size={20} color={theme.colors.cyan} strokeWidth={2.5} />
        </View>
        <View>
          <Text style={styles.brandTitle}>
            Fraud<Text style={styles.brandHighlight}>Shield</Text>
          </Text>
          <Text style={styles.brandSubtitle}>AI Real-Time Payment Guard</Text>
        </View>
      </View>

      <View style={styles.rightActions}>
        <Pressable 
          onPress={onOpenSettings} 
          style={({ pressed }) => [
            styles.statusPill, 
            pressed && { opacity: 0.7 }
          ]}
        >
          <View style={[
            styles.statusDot, 
            { backgroundColor: serverStatus === "online" ? theme.colors.emerald : theme.colors.rose }
          ]} />
          <Text style={styles.statusText}>
            {serverStatus === "online" ? "AI Live" : "Local Engine"}
          </Text>
          <Settings size={14} color={theme.colors.textMuted} style={{ marginLeft: 3 }} />
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.surfaceBorder,
  },
  brandRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  logoBadge: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "rgba(6, 182, 212, 0.12)",
    borderWidth: 1,
    borderColor: "rgba(6, 182, 212, 0.35)",
    alignItems: "center",
    justifyContent: "center",
  },
  brandTitle: {
    fontSize: 17,
    fontWeight: "900",
    color: "#ffffff",
    letterSpacing: -0.5,
  },
  brandHighlight: {
    color: theme.colors.cyan,
  },
  brandSubtitle: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    fontWeight: "600",
  },
  rightActions: {
    flexDirection: "row",
    alignItems: "center",
  },
  statusPill: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(15, 23, 42, 0.8)",
    paddingHorizontal: 8,
    paddingVertical: 5,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    gap: 4,
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: 4,
  },
  statusText: {
    fontSize: 10,
    fontWeight: "700",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
  },
});

