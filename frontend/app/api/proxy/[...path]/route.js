import { cookies } from 'next/headers'

const API_BASE = process.env.API_BASE_URL

async function getTokenFromCookies() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')?.value
  return token
}

async function proxyRequest(request, path, method) {
  try {
    const token = await getTokenFromCookies()
    if (!token) {
      return Response.json({ message: 'No token found' }, { status: 401 })
    }

    const url = new URL(request.url)
    const searchParams = url.searchParams
    const queryString = searchParams.toString()
    const backendUrl = `${API_BASE}${path}${queryString ? '?' + queryString : ''}`

    let body = null
    const contentType = request.headers.get('content-type')
    
    if (contentType?.includes('application/json') && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      body = JSON.stringify(await request.json())
    } else if (method !== 'GET' && method !== 'DELETE') {
      body = await request.text()
    }

    const response = await fetch(backendUrl, {
      method,
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body
    })

    const data = await response.text()
    let result = null
    try { result = data ? JSON.parse(data) : null } catch (e) { result = data }

    if (!response.ok) {
      return Response.json({ message: result?.message || 'Request failed' }, { status: response.status })
    }

    return Response.json(result)
  } catch (error) {
    console.error('Error in proxy request:', error)
    return Response.json({ message: 'Internal server error' }, { status: 500 })
  }
}

export async function GET(request, { params }) {
  const { path } = await params
  const fullPath = '/' + path.join('/')
  return proxyRequest(request, fullPath, 'GET')
}

export async function POST(request, { params }) {
  const { path } = await params
  const fullPath = '/' + path.join('/')
  return proxyRequest(request, fullPath, 'POST')
}

export async function PUT(request, { params }) {
  const { path } = await params
  const fullPath = '/' + path.join('/')
  return proxyRequest(request, fullPath, 'PUT')
}

export async function PATCH(request, { params }) {
  const { path } = await params
  const fullPath = '/' + path.join('/')
  return proxyRequest(request, fullPath, 'PATCH')
}

export async function DELETE(request, { params }) {
  const { path } = await params
  const fullPath = '/' + path.join('/')
  return proxyRequest(request, fullPath, 'DELETE')
}
