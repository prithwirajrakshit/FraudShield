import React, { useState, useEffect } from "react";
import { StyleSheet, View, Text, Pressable, Platform, StatusBar as RNStatusBar } from "react-native";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider, initialWindowMetrics, useSafeAreaInsets } from "react-native-safe-area-context";
import { ShieldAlert, FileText } from "lucide-react-native";
import { Navbar } from "./src/components/Navbar";
import { TransactionScreen } from "./src/components/TransactionScreen";
import { StatementScreen } from "./src/components/StatementScreen";
import { ServerConfigModal } from "./src/components/ServerConfigModal";
import { checkHealth } from "./src/lib/api";
import { theme } from "./src/styles/theme";

function MainApp() {
  const [activeTab, setActiveTab] = useState<"transaction" | "statement">("transaction");
  const [serverModalVisible, setServerModalVisible] = useState(false);
  const [serverStatus, setServerStatus] = useState<"online" | "offline" | "checking">("checking");
  const insets = useSafeAreaInsets();

  // Bulletproof notch / punch-hole / notification-bar clearance across all Android & iOS displays
  const androidBarHeight = RNStatusBar.currentHeight || 0;
  const topInset = Platform.OS === "android"
    ? Math.max(androidBarHeight, insets.top || 0, 38) + 6
    : Math.max(insets.top || 0, 20) + 4;

  useEffect(() => {
    checkHealth().then((res) => {
      setServerStatus(res.status === "healthy" ? "online" : "offline");
    });
  }, []);

  return (
    <View style={styles.rootContainer}>
      <StatusBar style="light" />
      
      {/* Top Safe Area Container for Status Bar & Punch-Hole clearance */}
      <View style={{ paddingTop: topInset, backgroundColor: theme.colors.surface }}>
        <Navbar 
          onOpenSettings={() => setServerModalVisible(true)} 
          serverStatus={serverStatus} 
        />
      </View>

      {/* Screen Content - Preserves state across tab switches */}
      <View style={styles.body}>
        <View style={[styles.screenWrapper, activeTab !== "transaction" && styles.screenHidden]}>
          <TransactionScreen />
        </View>
        <View style={[styles.screenWrapper, activeTab !== "statement" && styles.screenHidden]}>
          <StatementScreen />
        </View>
      </View>

      {/* Bottom Navigation Bar with Home Indicator Inset Clearance */}
      <View style={[styles.bottomNav, { paddingBottom: Math.max(insets.bottom, 12) + 6 }]}>
        
        <Pressable
          style={[styles.navItem, activeTab === "transaction" && styles.navItemActive]}
          onPress={() => setActiveTab("transaction")}
        >
          <View style={styles.navIconWrapper}>
            <ShieldAlert 
              size={20} 
              color={activeTab === "transaction" ? theme.colors.cyan : theme.colors.textSubtle} 
            />
          </View>
          <Text style={[styles.navText, activeTab === "transaction" && styles.navTextActive]}>
            Live Guard
          </Text>
        </Pressable>

        <Pressable
          style={[styles.navItem, activeTab === "statement" && styles.navItemActive]}
          onPress={() => setActiveTab("statement")}
        >
          <View style={styles.navIconWrapper}>
            <FileText 
              size={20} 
              color={activeTab === "statement" ? theme.colors.cyan : theme.colors.textSubtle} 
            />
          </View>
          <Text style={[styles.navText, activeTab === "statement" && styles.navTextActive]}>
            Statement Vault
          </Text>
        </Pressable>

      </View>

      {/* Backend Server Configuration Modal */}
      <ServerConfigModal
        visible={serverModalVisible}
        onClose={() => setServerModalVisible(false)}
        onServerUpdated={(status) => setServerStatus(status)}
      />

    </View>
  );
}

export default function App() {
  return (
    <SafeAreaProvider initialMetrics={initialWindowMetrics}>
      <MainApp />
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  rootContainer: {
    flex: 1,
    backgroundColor: theme.colors.bg,
  },
  body: {
    flex: 1,
    backgroundColor: theme.colors.bg,
  },
  screenWrapper: {
    flex: 1,
  },
  screenHidden: {
    display: "none",
  },
  bottomNav: {
    flexDirection: "row",
    backgroundColor: theme.colors.surface,
    borderTopWidth: 1,
    borderTopColor: theme.colors.surfaceBorder,
    paddingTop: 10,
    justifyContent: "space-around",
  },
  navItem: {
    alignItems: "center",
    justifyContent: "center",
    flex: 1,
    paddingVertical: 2,
  },
  navItemActive: {
    opacity: 1,
  },
  navIconWrapper: {
    marginBottom: 4,
  },
  navText: {
    fontSize: 10,
    fontWeight: "700",
    color: theme.colors.textSubtle,
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  navTextActive: {
    color: theme.colors.cyanLight,
  },
});
