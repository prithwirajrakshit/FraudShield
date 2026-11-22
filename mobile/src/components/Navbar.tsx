import React, { useEffect, useRef } from "react";
import { View, Text, StyleSheet, Pressable, Animated } from "react-native";
import { ShieldCheck, Settings } from "lucide-react-native";
import { theme } from "../styles/theme";

interface NavbarProps {
  onOpenSettings: () => void;
  serverStatus: "online" | "offline" | "checking";
}

export function Navbar({ onOpenSettings, serverStatus }: NavbarProps) {
  const pulseAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 0,
          duration: 1800,
          useNativeDriver: true,
        }),
      ])
    );
    animation.start();
    return () => animation.stop();
  }, [pulseAnim]);

  const auraOpacity = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0.35, 0.75],
  });

  const auraScale = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0.95, 1.15],
  });

  return (
    <View style={styles.container}>
      <View style={styles.brandRow}>
        <View style={styles.logoContainer}>
          <Animated.View
            style={[
              styles.logoAura,
              {
                opacity: auraOpacity,
                transform: [{ scale: auraScale }],
              },
            ]}
          />
          <View style={styles.logoBadge}>
            <ShieldCheck size={20} color={theme.colors.rose} strokeWidth={2.5} />
          </View>
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
  logoContainer: {
    position: "relative",
    width: 38,
    height: 38,
    alignItems: "center",
    justifyContent: "center",
  },
  logoAura: {
    position: "absolute",
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: "rgba(244, 63, 94, 0.4)",
    shadowColor: "#f43f5e",
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.85,
    shadowRadius: 10,
    elevation: 6,
  },
  logoBadge: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "rgba(244, 63, 94, 0.16)",
    borderWidth: 1.5,
    borderColor: "rgba(244, 63, 94, 0.7)",
    alignItems: "center",
    justifyContent: "center",
  },
  brandTitle: {
    fontSize: 16,
    fontWeight: "900",
    color: "#ffffff",
    letterSpacing: 1.2,
    textTransform: "uppercase",
  },
  brandHighlight: {
    color: theme.colors.roseLight,
  },
  brandSubtitle: {
    fontSize: 9.5,
    color: theme.colors.textSubtle,
    fontWeight: "700",
    letterSpacing: 0.5,
    textTransform: "uppercase",
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

