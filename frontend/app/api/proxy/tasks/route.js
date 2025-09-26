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

    // Forward query parameters
    const url = new URL(request.url)
    const searchParams = url.searchParams
    const queryString = searchParams.toString()
    const backendUrl = `${API_BASE}/tasks${queryString ? '?' + queryString : ''}`

    const response = await fetch(backendUrl, {
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
      return Response.json({ message: result?.message || 'Failed to fetch tasks' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error fetching tasks:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const body = await request.json()

    const response = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Failed to create task' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error creating task:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
