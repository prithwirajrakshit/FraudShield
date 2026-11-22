import React from "react";
import { View, Text, StyleSheet } from "react-native";
import Svg, { Circle, G, Defs, LinearGradient, Stop } from "react-native-svg";
import { CheckCircle2, AlertTriangle, ShieldAlert, Zap, Cpu, Radio } from "lucide-react-native";
import { SecurityAssessment } from "../lib/api";
import { theme } from "../styles/theme";
import { GlowCard } from "./GlowCard";

interface RiskGaugeProps {
  assessment: SecurityAssessment;
}

export function RiskGauge({ assessment }: RiskGaugeProps) {
  const percent = assessment.risk_score_percent;
  const status = assessment.status;

  const config = {
    APPROVED: {
      color: theme.colors.emerald,
      badgeBg: "rgba(6, 78, 59, 0.7)",
      badgeBorder: theme.colors.emerald,
      textColor: theme.colors.emeraldLight,
      icon: CheckCircle2,
      label: "Safe to Authorize",
      description: "Low-entropy behavioral signal. Parameters align with authenticated cardholder history."
    },
    CHALLENGE: {
      color: theme.colors.amber,
      badgeBg: "rgba(120, 53, 15, 0.7)",
      badgeBorder: theme.colors.amber,
      textColor: theme.colors.amberLight,
      icon: AlertTriangle,
      label: "Verification Required",
      description: "Elevated risk signals detected. Requires two-factor SMS passcode authentication."
    },
    BLOCKED: {
      color: theme.colors.rose,
      badgeBg: "rgba(136, 19, 55, 0.7)",
      badgeBorder: theme.colors.rose,
      textColor: theme.colors.roseLight,
      icon: ShieldAlert,
      label: "Fraud Intercepted",
      description: "Severe threat anomaly detected. Transaction intercepted at gateway to protect account funds."
    }
  }[status];

  const IconComponent = config.icon;

  const size = 170;
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percent / 100) * circumference;

  return (
    <GlowCard style={[styles.card, { borderColor: config.badgeBorder }]}>
      <View style={styles.content}>
        
        {/* Holographic Circular HUD Gauge */}
        <View style={styles.gaugeContainer}>
          <Svg width={size} height={size}>
            <Defs>
              <LinearGradient id="activeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <Stop offset="0%" stopColor={config.color} stopOpacity="1" />
                <Stop offset="100%" stopColor={theme.colors.cyan} stopOpacity="1" />
              </LinearGradient>
            </Defs>

            {/* Background Track */}
            <Circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              stroke="#1e293b"
              strokeWidth={strokeWidth}
              fill="transparent"
              strokeDasharray="4 6"
            />

            {/* Glowing Active Progress Arc */}
            <G rotation="-90" origin={`${size / 2}, ${size / 2}`}>
              <Circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                stroke="url(#activeGrad)"
                strokeWidth={strokeWidth}
                fill="transparent"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
              />
            </G>
          </Svg>

          {/* Central Digital Matrix Readout */}
          <View style={styles.centerTextContainer}>
            <Text style={styles.percentText}>{percent}%</Text>
            <View style={styles.labelRow}>
              <Radio size={10} color={theme.colors.cyan} />
              <Text style={styles.threatIndexLabel}>Threat Index</Text>
            </View>
          </View>
        </View>

        {/* Telemetry & Assessment Readout */}
        <View style={styles.telemetrySection}>
          
          <View style={styles.badgeRow}>
            <View style={[styles.statusBadge, { backgroundColor: config.badgeBg, borderColor: config.badgeBorder }]}>
              <IconComponent size={13} color={config.color} />
              <Text style={[styles.statusBadgeText, { color: config.textColor }]}>{status}</Text>
            </View>

            <View style={styles.pill}>
              <Zap size={11} color={theme.colors.cyan} />
              <Text style={styles.pillText}>{assessment.latency_ms}ms</Text>
            </View>

            <View style={styles.pill}>
              <Cpu size={11} color="#818cf8" />
              <Text style={styles.pillText}>Focal DNN</Text>
            </View>
          </View>

          <Text style={[styles.headline, { color: config.textColor }]}>
            {assessment.headline}
          </Text>

          <Text style={styles.description}>
            {config.description}
          </Text>
        </View>

      </View>
    </GlowCard>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.colors.surface,
    borderRadius: 20,
    borderWidth: 1.5,
    padding: 16,
    marginVertical: 10,
    overflow: "hidden",
  },
  content: {
    alignItems: "center",
  },
  gaugeContainer: {
    position: "relative",
    width: 170,
    height: 170,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  },
  centerTextContainer: {
    position: "absolute",
    alignItems: "center",
    justifyContent: "center",
  },
  percentText: {
    fontSize: 34,
    fontWeight: "900",
    color: "#ffffff",
    letterSpacing: -1,
  },
  labelRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    marginTop: 2,
  },
  threatIndexLabel: {
    fontSize: 9,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 1.2,
  },
  telemetrySection: {
    width: "100%",
    alignItems: "center",
  },
  badgeRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: 6,
    marginBottom: 10,
  },
  statusBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 5,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 20,
    borderWidth: 1,
  },
  statusBadgeText: {
    fontSize: 11,
    fontWeight: "800",
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  pill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "#0f172a",
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  pillText: {
    fontSize: 10,
    color: theme.colors.textMuted,
    fontWeight: "600",
  },
  headline: {
    fontSize: 18,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 6,
  },
  description: {
    fontSize: 12,
    color: theme.colors.textMuted,
    textAlign: "center",
    lineHeight: 18,
  },
});

