'use client'
import { useAuth } from '../hooks/useAuth'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push('/tasks')
    }
  }, [loading, user, router])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md mx-auto text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Welcome to Task Manager</h1>
        <div className="space-y-4">
          <a 
            href="/login" 
            className="block w-full bg-blue-600 text-white py-3 px-6 rounded hover:bg-blue-700 transition"
          >
            Login to Get Started
          </a>
          <a 
            href="/signup" 
            className="block w-full border border-gray-300 text-gray-700 py-3 px-6 rounded hover:bg-gray-50 transition"
          >
            Create Account
          </a>
        </div>
      </div>
    </div>
  )
}
