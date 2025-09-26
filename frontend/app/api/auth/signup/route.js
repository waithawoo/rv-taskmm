const API_BASE = process.env.API_BASE_URL

export async function POST(request) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${API_BASE}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Signup failed' }, { status: response.status })
    }

    const backendData = result.data || result
    const token = backendData.access_token
    
    const user = {
      id: backendData.id,
      name: backendData.name,
      email: backendData.email,
      role: backendData.role?.toLowerCase() || 'user'
    }

    const headers = new Headers()
    headers.set('Set-Cookie', `token=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${7 * 24 * 60 * 60}`)
    return Response.json({ user }, { headers })
  } catch (error) {
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
