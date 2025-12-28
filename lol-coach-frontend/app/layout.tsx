import type { Metadata } from "next";
import "./globals.css";

// Fonts are loaded via Google Fonts CDN in globals.css
// Rajdhani for headings (military-tech style), Inter for body text

export const metadata: Metadata = {
  title: "UNSC Tactical Command - Halo-Inspired LoL Strategy",
  description: "Military-grade tactical intelligence system - Real-time win prediction, operative analytics, and strategic loadout recommendations",
  icons: {
    icon: "/favicon.png",
    apple: "/logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <body
        className="antialiased"
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
