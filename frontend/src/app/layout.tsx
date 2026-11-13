import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FraudShield • Cyber-Obsidian AI Payment Security",
  description: "Next-generation real-time transaction fraud authorization & deep threat anomaly shield.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#070b14] text-slate-100 font-sans selection:bg-blue-500/30 selection:text-blue-200">
        {children}
      </body>
    </html>
  );
}
