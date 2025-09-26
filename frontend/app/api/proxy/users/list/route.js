import { cookies } from 'next/headers'

const API_BASE = process.env.API_BASE_URL

async function getTokenFromCookies() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')?.value
  return token
}

export async function GET(request) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const response = await fetch(`${API_BASE}/users/list`, {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Failed to fetch users' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error fetching users:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
