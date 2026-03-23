import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'GEOINT Portal',
  description: 'Geospatial Intelligence World View',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-tactical-bg text-white font-mono">{children}</body>
    </html>
  )
}
