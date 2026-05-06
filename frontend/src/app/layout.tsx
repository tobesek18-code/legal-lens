import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "LegaLens - AI-Powered Lease Review",
  description:
    "AI-powered document compliance review for rental agreements. Professional lease analysis with jurisdiction-specific legal insights.",
  keywords:
    "lease review, rental agreement, legal compliance, AI analysis, property law",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <Header />
        <main className="main-content flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
