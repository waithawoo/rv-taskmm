const API_BASE = process.env.API_BASE_URL

export async function POST(request) {
  try {
    const body = await request.json()
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    // console.log('response', response);

    const data = await response.text()
    
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Login failed' }, { status: response.status })
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
    const isProduction = process.env.NODE_ENV === 'production'
    const cookieOptions = [
      `token=${token}`,
      'HttpOnly',
      isProduction ? 'Secure' : '',
      'SameSite=Strict',
      'Path=/',
      `Max-Age=${7 * 24 * 60 * 60}`
    ].filter(Boolean).join('; ')
    
    headers.set('Set-Cookie', cookieOptions)
    
    return Response.json({ user }, { headers })
  } catch (error) {
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}
