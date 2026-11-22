import React, { useState, useEffect } from "react";
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TextInput, 
  Pressable, 
  Switch, 
  ActivityIndicator,
  Alert
} from "react-native";
import * as Haptics from "expo-haptics";
import { 
  IndianRupee, 
  Store, 
  Globe, 
  Moon, 
  Smartphone, 
  Sparkles, 
  SlidersHorizontal, 
  ShieldCheck, 
  AlertCircle,
  CheckCircle2,
  Lock
} from "lucide-react-native";
import { 
  TransactionCheckRequest, 
  TransactionCheckResponse, 
  Scenario, 
  checkTransaction, 
  getScenarios 
} from "../lib/api";
import { RiskGauge } from "./RiskGauge";
import { GlowCard } from "./GlowCard";
import { theme } from "../styles/theme";

export function TransactionScreen() {
  const [formData, setFormData] = useState<TransactionCheckRequest>({
    amount: 0,
    merchant_name: "",
    merchant_category: "dining",
    channel: "online",
    is_foreign: false,
    is_night_time: false,
    device_trusted: true,
    user_avg_amount: 50.0,
    velocity_1h: 1,
  });

  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TransactionCheckResponse | null>(null);

  useEffect(() => {
    getScenarios().then(setScenarios);
  }, []);

  const handleScan = async (overrideData?: TransactionCheckRequest) => {
    const dataToScan = overrideData || formData;
    if (dataToScan.amount <= 0) {
      Alert.alert("Enter Amount", "Please enter a transaction amount greater than ₹0 to scan.");
      return;
    }

    try {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    } catch (e) {}

    setLoading(true);
    try {
      const res = await checkTransaction(dataToScan);
      setResult(res);
      if (res.security_assessment.status === "BLOCKED") {
        try {
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
        } catch (e) {}
      } else if (res.security_assessment.status === "CHALLENGE") {
        try {
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
        } catch (e) {}
      } else {
        try {
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        } catch (e) {}
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyScenario = (sc: Scenario) => {
    setFormData(sc.data);
    try {
      Haptics.selectionAsync();
    } catch (e) {}
    handleScan(sc.data);
  };

  const categories = [
    { id: "dining", label: "Dining / Food" },
    { id: "grocery", label: "Grocery / Mart" },
    { id: "electronics", label: "Electronics" },
    { id: "crypto", label: "Crypto Asset" },
    { id: "travel", label: "Travel / Hotel" },
    { id: "transport", label: "Transport" },
    { id: "jewelry", label: "Luxury Jewelry" },
    { id: "general", label: "General Retail" },
  ];

  const channels = [
    { id: "online", label: "UPI / Online" },
    { id: "in_store_chip", label: "Chip & PIN" },
    { id: "contactless", label: "Tap & Pay" },
    { id: "atm", label: "Cash" },
  ];

  const quickAmounts = [20, 100, 500, 1500, 5000, 25000];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer} showsVerticalScrollIndicator={false}>
      
      {/* Risk Gauge Result if available */}
      {result && (
        <View style={styles.resultSection}>
          <RiskGauge assessment={result.security_assessment} />

          {/* Explanation Matrix Card */}
          <GlowCard style={styles.explanationCard}>
            <View style={styles.explHeader}>
              <ShieldCheck size={16} color={theme.colors.cyan} />
              <Text style={styles.explTitle}>GDPR Art. 22 Threat Attribution</Text>
            </View>

            {/* Risk factors */}
            {result.explanation.risk_factors.map((rf, idx) => (
              <View key={idx} style={styles.riskFactorRow}>
                <AlertCircle size={14} color={rf.type === "critical" ? theme.colors.rose : theme.colors.amber} style={{ marginTop: 2 }} />
                <View style={{ flex: 1 }}>
                  <Text style={[styles.rfTitle, { color: rf.type === "critical" ? theme.colors.roseLight : theme.colors.amberLight }]}>
                    {rf.title}
                  </Text>
                  <Text style={styles.rfDetail}>{rf.detail}</Text>
                </View>
              </View>
            ))}

            {/* Positive factors */}
            {result.explanation.safety_factors.map((sf, idx) => (
              <View key={idx} style={styles.safetyFactorRow}>
                <CheckCircle2 size={14} color={theme.colors.emerald} style={{ marginTop: 2 }} />
                <Text style={styles.sfText}>{sf}</Text>
              </View>
            ))}

            {/* Action recommendation */}
            <View style={styles.actionCard}>
              <Text style={styles.actionTitle}>{result.explanation.recommended_action.title}</Text>
              <Text style={styles.actionSummary}>{result.explanation.recommended_action.summary}</Text>
              {result.explanation.recommended_action.steps.map((step, idx) => (
                <Text key={idx} style={styles.actionStep}>• {step}</Text>
              ))}
            </View>
          </GlowCard>
        </View>
      )}

      {/* Preset Scenarios Carousel */}
      <View style={styles.sectionHeader}>
        <Sparkles size={14} color={theme.colors.cyan} />
        <Text style={styles.sectionTitle}>Test Scenarios</Text>
      </View>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.scenariosScroll}>
        {scenarios.map((sc) => (
          <Pressable
            key={sc.id}
            onPress={() => applyScenario(sc)}
            style={({ pressed }) => [styles.scenarioCard, pressed && { opacity: 0.8 }]}
          >
            <View style={styles.scRow}>
              <Text style={styles.scName} numberOfLines={1}>{sc.name}</Text>
              <Text style={styles.scAmt}>₹{sc.data.amount}</Text>
            </View>
            <Text style={styles.scDesc} numberOfLines={2}>{sc.description}</Text>
          </Pressable>
        ))}
      </ScrollView>

      {/* Main Input Form */}
      <GlowCard style={styles.formCard}>
        
        {/* Amount Input */}
        <Text style={styles.fieldLabel}>Transaction Amount (₹)</Text>
        <View style={styles.amountInputRow}>
          <IndianRupee size={20} color={theme.colors.cyan} />
          <TextInput
            style={styles.amountInput}
            keyboardType="numeric"
            value={formData.amount === 0 ? "" : formData.amount.toString()}
            onChangeText={(v) => {
              const cleaned = v.replace(/[^0-9.]/g, "");
              setFormData({ ...formData, amount: parseFloat(cleaned) || 0 });
            }}
            placeholder="0"
            placeholderTextColor={theme.colors.textSubtle}
          />
        </View>

        {/* Quick Amount Pills */}
        <View style={styles.quickAmtRow}>
          {quickAmounts.map((amt) => (
            <Pressable
              key={amt}
              onPress={() => setFormData({ ...formData, amount: amt })}
              style={[styles.quickAmtPill, formData.amount === amt && styles.quickAmtPillActive]}
            >
              <Text style={[styles.quickAmtText, formData.amount === amt && styles.quickAmtTextActive]}>
                ₹{amt}
              </Text>
            </Pressable>
          ))}
        </View>

        {/* Merchant Name */}
        <Text style={styles.fieldLabel}>Merchant Entity</Text>
        <View style={styles.textInputRow}>
          <Store size={16} color={theme.colors.textMuted} />
          <TextInput
            style={styles.textInput}
            value={formData.merchant_name}
            onChangeText={(v) => setFormData({ ...formData, merchant_name: v })}
            placeholder="Store, App or Payee Name"
            placeholderTextColor={theme.colors.textSubtle}
          />
        </View>

        {/* Category Pills */}
        <Text style={styles.fieldLabel}>Industry / Sector</Text>
        <View style={styles.pillsWrap}>
          {categories.map((c) => (
            <Pressable
              key={c.id}
              onPress={() => setFormData({ ...formData, merchant_category: c.id })}
              style={[styles.choicePill, formData.merchant_category === c.id && styles.choicePillActive]}
            >
              <Text style={[styles.choicePillText, formData.merchant_category === c.id && styles.choicePillTextActive]}>
                {c.label}
              </Text>
            </Pressable>
          ))}
        </View>

        {/* Channel Pills */}
        <Text style={styles.fieldLabel}>Payment Channel</Text>
        <View style={styles.pillsWrap}>
          {channels.map((ch) => (
            <Pressable
              key={ch.id}
              onPress={() => setFormData({ ...formData, channel: ch.id })}
              style={[styles.choicePill, formData.channel === ch.id && styles.choicePillActive]}
            >
              <Text style={[styles.choicePillText, formData.channel === ch.id && styles.choicePillTextActive]}>
                {ch.label}
              </Text>
            </Pressable>
          ))}
        </View>

        {/* Security Context Toggles */}
        <Text style={styles.fieldLabel}>Behavioral Anomaly Toggles</Text>
        
        <View style={styles.toggleRow}>
          <View style={styles.toggleLabelGroup}>
            <Globe size={16} color={theme.colors.cyan} />
            <View>
              <Text style={styles.toggleTitle}>Overseas / Foreign IP</Text>
              <Text style={styles.toggleSub}>Cross-border gateway routing</Text>
            </View>
          </View>
          <Switch
            value={formData.is_foreign}
            onValueChange={(v) => setFormData({ ...formData, is_foreign: v })}
            trackColor={{ false: "#1e293b", true: theme.colors.cyan }}
            thumbColor={formData.is_foreign ? "#ffffff" : "#64748b"}
          />
        </View>

        <View style={styles.toggleRow}>
          <View style={styles.toggleLabelGroup}>
            <Moon size={16} color={theme.colors.amber} />
            <View>
              <Text style={styles.toggleTitle}>Night Hours (1 AM - 5 AM)</Text>
              <Text style={styles.toggleSub}>Off-peak authorization window</Text>
            </View>
          </View>
          <Switch
            value={formData.is_night_time}
            onValueChange={(v) => setFormData({ ...formData, is_night_time: v })}
            trackColor={{ false: "#1e293b", true: theme.colors.amber }}
            thumbColor={formData.is_night_time ? "#ffffff" : "#64748b"}
          />
        </View>

        <View style={styles.toggleRow}>
          <View style={styles.toggleLabelGroup}>
            <Smartphone size={16} color={theme.colors.emerald} />
            <View>
              <Text style={styles.toggleTitle}>Trusted Mobile Device</Text>
              <Text style={styles.toggleSub}>Hardware token & biometric verified</Text>
            </View>
          </View>
          <Switch
            value={formData.device_trusted}
            onValueChange={(v) => setFormData({ ...formData, device_trusted: v })}
            trackColor={{ false: "#1e293b", true: theme.colors.emerald }}
            thumbColor={formData.device_trusted ? "#ffffff" : "#64748b"}
          />
        </View>

        {/* Cardholder Historical Average Spend */}
        <View style={styles.avgSpendCard}>
          <View style={styles.avgSpendHeader}>
            <View style={{ flexDirection: "row", alignItems: "center", gap: 6 }}>
              <SlidersHorizontal size={14} color={theme.colors.cyan} />
              <Text style={styles.avgSpendTitle}>Cardholder Typical Average</Text>
            </View>
          </View>

          {/* Editable Custom Average Input */}
          <View style={styles.avgInputRow}>
            <IndianRupee size={16} color={theme.colors.cyan} />
            <TextInput
              style={styles.avgInput}
              keyboardType="numeric"
              value={formData.user_avg_amount === 0 ? "" : formData.user_avg_amount.toString()}
              onChangeText={(v) => {
                const cleaned = v.replace(/[^0-9.]/g, "");
                setFormData({ ...formData, user_avg_amount: parseFloat(cleaned) || 0 });
              }}
              placeholder="e.g. 50"
              placeholderTextColor={theme.colors.textSubtle}
            />
          </View>

          {/* Quick preset pills */}
          <View style={styles.avgQuickRow}>
            {[50, 150, 500, 1500].map((avg) => (
              <Pressable
                key={avg}
                onPress={() => setFormData({ ...formData, user_avg_amount: avg })}
                style={[styles.avgPill, formData.user_avg_amount === avg && styles.avgPillActive]}
              >
                <Text style={[styles.avgPillText, formData.user_avg_amount === avg && styles.avgPillTextActive]}>
                  ₹{avg}
                </Text>
              </Pressable>
            ))}
          </View>
        </View>

        {/* Scan Button */}
        <Pressable
          style={({ pressed }) => [styles.scanButton, pressed && { opacity: 0.85 }]}
          onPress={() => handleScan()}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#030712" />
          ) : (
            <>
              <ShieldCheck size={18} color="#030712" strokeWidth={2.5} />
              <Text style={styles.scanButtonText}>Scan Payment with Deep Focal AI</Text>
            </>
          )}
        </Pressable>

      </GlowCard>

    </ScrollView>
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
  resultSection: {
    marginBottom: 16,
  },
  explanationCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 16,
    marginTop: 8,
  },
  explHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 12,
  },
  explTitle: {
    fontSize: 12,
    fontWeight: "800",
    color: theme.colors.cyan,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  riskFactorRow: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 8,
  },
  rfTitle: {
    fontSize: 12,
    fontWeight: "700",
  },
  rfDetail: {
    fontSize: 11,
    color: theme.colors.textMuted,
    marginTop: 2,
  },
  safetyFactorRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 6,
  },
  sfText: {
    fontSize: 11,
    color: theme.colors.textMuted,
  },
  actionCard: {
    backgroundColor: "#030712",
    borderRadius: 12,
    padding: 12,
    marginTop: 10,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  actionTitle: {
    fontSize: 13,
    fontWeight: "800",
    color: "#ffffff",
    marginBottom: 2,
  },
  actionSummary: {
    fontSize: 11,
    color: theme.colors.textMuted,
    marginBottom: 6,
  },
  actionStep: {
    fontSize: 10,
    color: theme.colors.cyanLight,
    marginTop: 2,
  },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  scenariosScroll: {
    marginBottom: 16,
  },
  scenarioCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 12,
    width: 200,
    marginRight: 10,
  },
  scRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  scName: {
    fontSize: 12,
    fontWeight: "800",
    color: "#ffffff",
    flex: 1,
    marginRight: 6,
  },
  scAmt: {
    fontSize: 11,
    fontWeight: "800",
    color: theme.colors.cyan,
  },
  scDesc: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    lineHeight: 14,
  },
  formCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    padding: 18,
  },
  fieldLabel: {
    fontSize: 11,
    fontWeight: "800",
    color: theme.colors.textMuted,
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginTop: 12,
    marginBottom: 8,
  },
  amountInputRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#030712",
    borderRadius: 14,
    borderWidth: 1.5,
    borderColor: "rgba(6, 182, 212, 0.4)",
    paddingHorizontal: 14,
    height: 54,
  },
  amountInput: {
    flex: 1,
    color: "#ffffff",
    fontSize: 22,
    fontWeight: "800",
    marginLeft: 10,
  },
  quickAmtRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
    marginTop: 8,
  },
  quickAmtPill: {
    backgroundColor: "#0f172a",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  quickAmtPillActive: {
    backgroundColor: "rgba(6, 182, 212, 0.2)",
    borderColor: theme.colors.cyan,
  },
  quickAmtText: {
    fontSize: 11,
    fontWeight: "700",
    color: theme.colors.textMuted,
  },
  quickAmtTextActive: {
    color: theme.colors.cyanLight,
  },
  textInputRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#030712",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    paddingHorizontal: 12,
    height: 44,
  },
  textInput: {
    flex: 1,
    color: "#ffffff",
    fontSize: 13,
    marginLeft: 8,
  },
  pillsWrap: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  choicePill: {
    backgroundColor: "#0f172a",
    paddingHorizontal: 10,
    paddingVertical: 7,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  choicePillActive: {
    backgroundColor: "rgba(6, 182, 212, 0.2)",
    borderColor: theme.colors.cyan,
  },
  choicePillText: {
    fontSize: 11,
    fontWeight: "600",
    color: theme.colors.textMuted,
  },
  choicePillTextActive: {
    color: theme.colors.cyanLight,
    fontWeight: "800",
  },
  toggleRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(30, 41, 59, 0.5)",
  },
  toggleLabelGroup: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    flex: 1,
  },
  toggleTitle: {
    fontSize: 12,
    fontWeight: "700",
    color: "#ffffff",
  },
  toggleSub: {
    fontSize: 10,
    color: theme.colors.textSubtle,
    marginTop: 1,
  },
  avgSpendCard: {
    backgroundColor: "#030712",
    borderRadius: 14,
    padding: 12,
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
    marginTop: 14,
    marginBottom: 16,
  },
  avgSpendHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  avgSpendTitle: {
    fontSize: 11,
    fontWeight: "700",
    color: theme.colors.textMuted,
  },
  avgInputRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#0a1120",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "rgba(6, 182, 212, 0.3)",
    paddingHorizontal: 10,
    height: 42,
    marginBottom: 10,
  },
  avgInput: {
    flex: 1,
    color: theme.colors.cyanLight,
    fontSize: 15,
    fontWeight: "800",
    marginLeft: 6,
  },
  avgQuickRow: {
    flexDirection: "row",
    gap: 6,
  },
  avgPill: {
    flex: 1,
    backgroundColor: "#0f172a",
    paddingVertical: 5,
    borderRadius: 8,
    alignItems: "center",
    borderWidth: 1,
    borderColor: theme.colors.surfaceBorder,
  },
  avgPillActive: {
    borderColor: theme.colors.cyan,
    backgroundColor: "rgba(6, 182, 212, 0.15)",
  },
  avgPillText: {
    fontSize: 11,
    color: theme.colors.textMuted,
    fontWeight: "700",
  },
  avgPillTextActive: {
    color: theme.colors.cyan,
  },
  scanButton: {
    backgroundColor: theme.colors.cyan,
    borderRadius: 14,
    paddingVertical: 14,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    shadowColor: theme.colors.cyan,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 8,
    elevation: 4,
  },
  scanButtonText: {
    fontSize: 13,
    fontWeight: "900",
    color: "#030712",
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
});

