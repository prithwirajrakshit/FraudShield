import React, { useRef, useState } from "react";
import { View, StyleSheet, Animated, GestureResponderEvent, ViewProps } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { theme } from "../styles/theme";

interface GlowCardProps extends ViewProps {
  children: React.ReactNode;
  style?: any;
  showSheen?: boolean;
}

export function GlowCard({
  children,
  style,
  showSheen = true,
  ...props
}: GlowCardProps) {
  const glowOpacity = useRef(new Animated.Value(0)).current;
  const [touchPos, setTouchPos] = useState({ x: 0, y: 0 });

  const handleTouchStart = (e: GestureResponderEvent) => {
    const { locationX, locationY } = e.nativeEvent;
    setTouchPos({ x: locationX, y: locationY });
    Animated.timing(glowOpacity, {
      toValue: 1,
      duration: 120,
      useNativeDriver: true,
    }).start();
  };

  const handleTouchMove = (e: GestureResponderEvent) => {
    const { locationX, locationY } = e.nativeEvent;
    setTouchPos({ x: locationX, y: locationY });
  };

  const handleTouchEnd = () => {
    Animated.timing(glowOpacity, {
      toValue: 0,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  return (
    <View
      style={[styles.container, style]}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
      {...props}
    >
      {/* Ambient Emerald Sheen */}
      {showSheen && (
        <LinearGradient
          colors={["rgba(16, 185, 129, 0.10)", "rgba(16, 185, 129, 0.02)", "transparent"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0.8 }}
          style={StyleSheet.absoluteFill}
          pointerEvents="none"
        />
      )}

      {/* Interactive Touch-Tracking Greenish Spotlight */}
      <Animated.View
        pointerEvents="none"
        style={[
          styles.touchSpotlight,
          {
            transform: [
              { translateX: touchPos.x - 80 },
              { translateY: touchPos.y - 80 },
            ],
            opacity: glowOpacity,
          },
        ]}
      >
        <LinearGradient
          colors={["rgba(16, 185, 129, 0.32)", "rgba(16, 185, 129, 0.10)", "transparent"]}
          style={styles.spotlightGradient}
          start={{ x: 0.5, y: 0.5 }}
          end={{ x: 1, y: 1 }}
        />
      </Animated.View>

      {/* Card Content */}
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.28)",
    overflow: "hidden",
    position: "relative",
  },
  touchSpotlight: {
    position: "absolute",
    top: 0,
    left: 0,
    width: 160,
    height: 160,
    borderRadius: 80,
    overflow: "hidden",
    zIndex: 1,
  },
  spotlightGradient: {
    width: "100%",
    height: "100%",
  },
});
