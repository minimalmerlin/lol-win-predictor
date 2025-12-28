import type { Metadata } from "next";
import "./globals.css";

// Fonts are loaded via Google Fonts CDN in globals.css
// Rajdhani for headings (military-tech style), Inter for body text

export const metadata: Metadata = {
  title: "GAMING WAR ROOM - AI Victory System",
  description: "Elite gaming intelligence platform - Deploy AI-powered match analytics, player intel, and adaptive build strategies for competitive domination",
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
