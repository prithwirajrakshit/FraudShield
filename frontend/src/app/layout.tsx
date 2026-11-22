import type { Metadata } from "next";
import { Space_Grotesk, Space_Mono, Orbitron } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  display: "swap",
});

const spaceMono = Space_Mono({
  weight: ["400", "700"],
  subsets: ["latin"],
  variable: "--font-space-mono",
  display: "swap",
});

const orbitron = Orbitron({
  subsets: ["latin"],
  variable: "--font-orbitron",
  display: "swap",
});

export const metadata: Metadata = {
  title: "FraudShield | Real-Time Payment Security Console",
  description: "Enterprise payment fraud prevention and universal bank statement security scanner.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`dark h-full overflow-x-clip antialiased ${spaceGrotesk.variable} ${spaceMono.variable} ${orbitron.variable}`}>
      <body className="min-h-full flex flex-col font-sans bg-[var(--bg-canvas)] text-[var(--text-primary)] overflow-x-clip">
        {children}
      </body>
    </html>
  );
}
