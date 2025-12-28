import type { Metadata } from "next";
import "./globals.css";

// Fonts are loaded via Google Fonts CDN in globals.css
// Chakra Petch for headings, Inter for body text

export const metadata: Metadata = {
  title: "LoL Coach - AI-Powered Win Prediction",
  description: "Real-time win prediction, champion analytics, and intelligent item recommendations for League of Legends",
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
