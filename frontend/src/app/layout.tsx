import type { Metadata } from "next";
import "./globals.css";
import { QueryProvider } from "@/components/Providers/QueryProvider";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "Bernie-SPSS — Web Statistical Software",
  description: "Open-source web-based statistical software for Vietnamese economics students",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body>
        <QueryProvider>
          {children}
          <Toaster richColors position="top-right" />
        </QueryProvider>
      </body>
    </html>
  );
}
