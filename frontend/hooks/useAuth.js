'use client'
import { createContext, useContext, useEffect, useState } from 'react'
import request from '../lib/api'
import TokenManager from '../lib/tokenManager'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchMe() {
      try {
        const me = await request('/api/auth/me')
        setUser(me)
        TokenManager.startAutoRefresh()
      } catch (err) {
        setUser(null)
        TokenManager.stopAutoRefresh()
      } finally {
        setLoading(false)
      }
    }
    fetchMe()
  }, [])

  async function login({ email, password }) {
    const data = await request('/api/auth/login', { method: 'POST', body: { email, password } })
    setUser(data.user)
    setLoading(false)
    TokenManager.startAutoRefresh()
    return data
  }

  async function signup({ name, email, password }) {
    const data = await request('/api/auth/signup', { method: 'POST', body: { name, email, password } })
    setLoading(false)
    return data
  }

  const logout = async () => {
    await request('/api/auth/logout', { method: 'POST' })
    TokenManager.stopAutoRefresh()
    setUser(null)
  }

  const refreshToken = async () => {
    try {
      await request('/api/auth/refresh', { method: 'POST' })
      return true
    } catch (error) {
      console.error('Manual token refresh failed:', error)
      TokenManager.stopAutoRefresh()
      setUser(null)
      return false
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
