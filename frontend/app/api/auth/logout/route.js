export async function POST(request) {
  const headers = new Headers()
  const isProduction = process.env.NODE_ENV === 'production'
  const cookieOptions = [
    'token=',
    'HttpOnly',
    isProduction ? 'Secure' : '',
    'SameSite=Strict',
    'Path=/',
    'Max-Age=0'
  ].filter(Boolean).join('; ')
  
  headers.set('Set-Cookie', cookieOptions)
  
  return Response.json({ message: 'Logged out successfully' }, { headers })
}
