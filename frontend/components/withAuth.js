'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../hooks/useAuth'

export default function withAuth(Component) {
  return function ProtectedPage(props) {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
      if (!loading && !user) {
        router.replace('/login')
      }
    }, [loading, user, router])

    if (loading) {
      return <div className="text-center py-8">Loading...</div>
    }
    
    if (!user) {
      return null
    }

    return <Component {...props} />
  }
}
