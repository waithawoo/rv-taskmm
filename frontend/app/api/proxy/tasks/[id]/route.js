import { cookies } from 'next/headers'

const API_BASE = process.env.API_BASE_URL

async function getTokenFromCookies() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')?.value
  return token
}

export async function PATCH(request, { params }) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const { id } = await params
    const body = await request.json()

    const response = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PATCH',
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
      return Response.json({ message: result?.message || 'Failed to update task' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error updating task:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}

export async function DELETE(request, { params }) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const { id } = await params

    const response = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'DELETE',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Failed to delete task' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error deleting task:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}

export async function GET(request, { params }) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const { id } = await params

    const response = await fetch(`${API_BASE}/tasks/${id}`, {
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
      return Response.json({ message: result?.message || 'Failed to fetch task' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error fetching task:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
