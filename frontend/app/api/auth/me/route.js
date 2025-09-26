import { cookies } from 'next/headers'

const API_BASE = process.env.API_BASE_URL

export async function GET(request) {
  try {
    const cookieStore = await cookies()
    const token = cookieStore.get('token')?.value

    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const response = await fetch(`${API_BASE}/auth/profile`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.text()
    
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Authentication failed' }, { status: response.status })
    }

    const backendData = result.data || result
    
    let user
    if (result.success && result.data) {
      user = {
        id: backendData.id,
        name: backendData.name,
        email: backendData.email,
        role: backendData.role?.toLowerCase() || 'user',
        created_at: backendData.created_at,
        updated_at: backendData.updated_at
      }
    } else {
      user = result
    }

    return Response.json(user)
  } catch (error) {
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
