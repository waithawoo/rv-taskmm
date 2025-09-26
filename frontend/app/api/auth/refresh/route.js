import { cookies } from 'next/headers'

const API_BASE = process.env.API_BASE_URL

export async function POST(request) {
  try {
    const cookieStore = await cookies()
    const token = cookieStore.get('token')?.value

    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const response = await fetch(`${API_BASE}/auth/refresh_token`, {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Token refresh failed' }, { status: response.status })
    }

    const backendData = result.data || result
    const newToken = backendData.access_token

    const headers = new Headers()
    const isProduction = process.env.NODE_ENV === 'production'
    const cookieOptions = [
      `token=${newToken}`,
      'HttpOnly',
      isProduction ? 'Secure' : '',
      'SameSite=Strict',
      'Path=/',
      `Max-Age=${7 * 24 * 60 * 60}` // 7 days
    ].filter(Boolean).join('; ')
    
    headers.set('Set-Cookie', cookieOptions)
    
    return Response.json({ 
      message: 'Token refreshed successfully',
      expires_at: backendData.expires_at 
    }, { headers })
  } catch (error) {
    console.error('Error refreshing token:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
