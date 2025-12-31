import type { Metadata } from "next";
import "./globals.css";
import AppShell from "@/components/layout/AppShell";

// Fonts are loaded via Google Fonts CDN in globals.css
// Rajdhani for headings, Inter for body text

export const metadata: Metadata = {
  title: "Hextech Data Pro - AI Victory System",
  description: "Professional gaming analytics platform - AI-powered match insights, player statistics, and data-driven strategies for competitive advantage",
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
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
