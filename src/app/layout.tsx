import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Doomslang Language",
  description: "A custom, strictly-typed, dynamically evaluated scripting language. Built from scratch with a robust type-checker, OOP support, and expressive syntax.",
  keywords: ["dooms", "programming language", "scripting language", "Rohan Shinde", "python", "oop"],
  authors: [{ name: "Rohan Shinde", url: "https://github.com/Rohan-Shinde24" }],
  openGraph: {
    title: "Doomslang Programming Language",
    description: "A custom, strictly-typed, dynamically evaluated scripting language. Built from scratch with a robust type-checker, OOP support, and expressive syntax.",
    url: "https://github.com/Rohan-Shinde24/Dooms",
    siteName: "Doomslang",
    type: "website",
    images: [
      {
        url: "/image.png",
        width: 1200,
        height: 630,
        alt: "Doomslang Programming Language Preview",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Doomslang Programming Language",
    description: "A custom, strictly-typed, dynamically evaluated scripting language. Built from scratch with a robust type-checker, OOP support, and expressive syntax.",
    images: ["/image.png"],
  },
  icons: {
    icon: "/image.png",
  },
};

import Galaxy from "./components/Galaxy";

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} antialiased`}
    >
      <body className="bg-transparent">
        <div className="fixed inset-0 z-[-1] pointer-events-auto">
          <Galaxy 
            mouseRepulsion={true}
            mouseInteraction={true}
            density={2.3}
            glowIntensity={0.5}
            saturation={0.2}
            hueShift={120}
            rotationSpeed={0.15}
            repulsionStrength={3.5}
            starSpeed={0.7}
            speed={0.9}
          />
        </div>
        {children}
      </body>
    </html>
  );
}
