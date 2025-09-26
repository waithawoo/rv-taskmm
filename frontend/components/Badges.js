export function StatusBadge({ status }) {
  const styles = {
    'TODO': 'bg-gray-200 text-gray-600 border-gray-300',
    'IN_PROGRESS': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'DONE': 'bg-green-100 text-green-800 border-green-200'
  }

  return (
    <span className={`inline-block px-1.5 py-0.5 text-2xs rounded border ${styles[status] || styles.TODO}`} style={{ fontSize: '10px' }}>
      {status === 'IN_PROGRESS' ? 'IN PROGRESS' : status}
    </span>
  )
}

export function PriorityBadge({ priority }) {
  const styles = {
    'LOW': 'bg-green-50 text-green-700 border-green-200',
    'MEDIUM': 'bg-yellow-50 text-yellow-700 border-yellow-200', 
    'HIGH': 'bg-red-50 text-red-700 border-red-200'
  }

  return (
    <span className={`inline-block px-1.5 py-0.5 text-2xs rounded border ${styles[priority] || styles.LOW}`} style={{ fontSize: '10px' }}>
      {priority}
    </span>
  )
}
