'use client'
import Nav from '../components/Nav'
import { AuthProvider } from '../hooks/useAuth'
import './globals.css'

export default function RootLayout({ children }) {
  return (
    <AuthProvider>
      <html lang="en">
        <body className="min-h-screen bg-gray-50">
          <Nav />
          <main className="max-w-4xl mx-auto py-8 px-4">
            {children}
          </main>
        </body>
      </html>
    </AuthProvider>
  )
}
