export default async function request(path, { method = 'GET', body, qs } = {}) {
  let apiPath = path
  if (!path.startsWith('/api')) {
    apiPath = `/api/proxy${path}`
  }
  
  const url = new URL(apiPath, window.location.origin)
  if (qs) Object.keys(qs).forEach(k => url.searchParams.append(k, qs[k]))

  const headers = { 'Accept': 'application/json' }
  if (body && !(body instanceof FormData)) headers['Content-Type'] = 'application/json'

  const makeRequest = async () => {
    const res = await fetch(url.toString(), {
      method,
      headers,
      body: body && !(body instanceof FormData) ? JSON.stringify(body) : body,
      credentials: 'include',
    })

    const text = await res.text()
    let data = null
    try { data = text ? JSON.parse(text) : null } catch (e) { data = text }

    return { res, data }
  }

  let { res, data } = await makeRequest()

  if (res.status === 401 && !path.includes('/api/auth/')) {
    try {
      const refreshResponse = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
      })
      
      if (refreshResponse.ok) {
        const retry = await makeRequest()
        res = retry.res
        data = retry.data
      }
    } catch (refreshError) {
      console.error('Token refresh failed:', refreshError)
    }
  }

  if (!res.ok) {
    const err = new Error((data && data.message) || res.statusText || 'API error')
    err.status = res.status
    err.data = data
    throw err
  }
  return data
}
