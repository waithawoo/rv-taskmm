'use client'

export default function FilterBar({ 
  filters, 
  onFilterChange, 
  onClearFilters, 
  onAddTask, 
  users = [],
  user
}) {
  const isAdmin = user?.role === 'admin'

  return (
    <div className="bg-white rounded p-3 flex flex-wrap items-center gap-3 mb-3 border">
      <input 
        type="text" 
        placeholder="Search..." 
        className="border px-2 py-1 rounded text-sm w-32"
        value={filters.search}
        onChange={(e) => onFilterChange('search', e.target.value)}
      />
      
      <select 
        className="border px-2 py-1 rounded text-sm"
        value={filters.status}
        onChange={(e) => onFilterChange('status', e.target.value)}
      >
        <option value="">All Status</option>
        <option value="TODO">TODO</option>
        <option value="IN_PROGRESS">IN PROGRESS</option>
        <option value="DONE">DONE</option>
      </select>
      
      <select 
        className="border px-2 py-1 rounded text-sm"
        value={filters.priority}
        onChange={(e) => onFilterChange('priority', e.target.value)}
      >
        <option value="">All Priority</option>
        <option value="LOW">LOW</option>
        <option value="MEDIUM">MEDIUM</option>
        <option value="HIGH">HIGH</option>
      </select>
      
      <select 
        className="border px-2 py-1 rounded text-sm"
        value={filters.assignee}
        onChange={(e) => onFilterChange('assignee', e.target.value)}
      >
        <option value="">All Assignees</option>
        {users.map(u => (
          <option key={u.id} value={u.id}>{u.name || u.email}</option>
        ))}
      </select>
      
      <button 
        onClick={onClearFilters}
        className="text-xs text-blue-600 bg-blue-50 border border-blue-200 hover:bg-blue-100 px-3 py-1 rounded transition"
        title="Clear all filters"
      >
        Clear
      </button>
      
      <div className="ml-auto">
        {isAdmin && (
          <button 
            onClick={onAddTask}
            className="flex items-center gap-1 bg-green-500 text-white text-sm px-3 py-1 rounded hover:bg-green-600 transition"
            title="Add new task"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Task
          </button>
        )}
      </div>
    </div>
  )
}
