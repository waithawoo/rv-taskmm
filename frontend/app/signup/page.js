'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../hooks/useAuth'
import Link from 'next/link'

export default function SignupPage() {
  const { signup } = useAuth()
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      await signup({ name, email, password })
      router.push('/tasks')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="w-full max-w-xs bg-white p-6 rounded shadow">
        <h1 className="text-xl font-bold text-center mb-4">Create Account</h1>
        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-sm font-medium">Name</label>
            <input 
              value={name} 
              onChange={e => setName(e.target.value)} 
              placeholder="Your name" 
              className="w-full border px-2 py-1 rounded" 
              required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Email</label>
            <input 
              value={email} 
              onChange={e => setEmail(e.target.value)} 
              placeholder="Email" 
              type="email" 
              className="w-full border px-2 py-1 rounded" 
              required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Password</label>
            <input 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
              placeholder="Password" 
              type="password" 
              className="w-full border px-2 py-1 rounded" 
              required 
            />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
            Sign Up
          </button>
        </form>
        <div className="text-center mt-3">
          <Link href="/login" className="text-blue-600 text-sm hover:underline">
            Already have an account? Login
          </Link>
        </div>
      </div>
    </div>
  )
}
