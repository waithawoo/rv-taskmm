export class TokenManager {
  static refreshInterval = null
  static isRefreshing = false

  static startAutoRefresh() {
    if (this.refreshInterval) return

    this.refreshInterval = setInterval(async () => {
      await this.refreshToken()
    }, 50 * 60 * 1000) // 50 minutes
  }

  static stopAutoRefresh() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
      this.refreshInterval = null
    }
  }

  static async refreshToken() {
    if (this.isRefreshing) return

    this.isRefreshing = true
    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
      })

      if (response.ok) {
        console.log('Token refreshed successfully')
        return true
      } else {
        console.warn('Token refresh failed:', response.statusText)
        return false
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      return false
    } finally {
      this.isRefreshing = false
    }
  }
}

if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    TokenManager.startAutoRefresh()
  })
  window.addEventListener('beforeunload', () => {
    TokenManager.stopAutoRefresh()
  })
}

export default TokenManager
