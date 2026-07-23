import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PL Geo Analytics",
  description: "英超地理探索与球员数据分析平台",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
