'use client'
import Link from 'next/link'
import { useAuth } from '../hooks/useAuth'

export default function Nav() {
  const { user, logout, loading } = useAuth()

  return (
    <nav className="flex justify-between items-center p-3 border-b border-gray-300 bg-white">
      <div className="flex items-center gap-4">
        <Link href="/" className="font-bold text-lg text-gray-800">Task Manager</Link>
      </div>
      <div className="flex items-center gap-3">
        {loading ? (
          <div className="text-sm text-gray-600">Loading...</div>
        ) : user ? (
          <>
            <span className="text-sm text-gray-600">Hi, {user.name || user.email || 'User'}</span>
            <button 
              onClick={logout} 
              className="px-3 py-1 rounded border border-gray-300 text-gray-600 hover:bg-gray-100"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-blue-600 hover:underline">Login</Link>
            <Link href="/signup" className="px-3 py-1 rounded bg-blue-600 text-white hover:bg-blue-700">
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
