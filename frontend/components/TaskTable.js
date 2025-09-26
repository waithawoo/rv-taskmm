'use client'
import { StatusBadge, PriorityBadge } from './Badges'

export default function TaskTable({ 
  tasks, 
  onSort, 
  sortBy, 
  sortDir,
  onEditTask,
  onDeleteTask,
  onViewTask,
  users = [],
  user
}) {
  const isAdmin = user?.role === 'admin'

  const getUserName = (userId) => {
    if (!userId) return '-'
    const u = users.find(user => user.id === userId)
    return u ? (u.name || u.email) : `User ${userId}`
  }

  const canEdit = (task) => {
    if (!user?.id || !task) return false
    return isAdmin || Number(task.assignee_id) === Number(user.id)
  }

  const canDelete = () => {
    return isAdmin
  }

  const handleSort = (field) => {
    onSort(field)
  }

  const formatDate = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString()
  }

  const formatDateTime = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleString()
  }

  return (
    <div className="overflow-x-auto bg-white rounded shadow border">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-100 text-gray-600 text-xs">
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-1/6" 
              onClick={() => handleSort('title')}
            >
              Title {sortBy === 'title' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-1/3" 
              onClick={() => handleSort('description')}
            >
              Description {sortBy === 'description' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-24" 
              onClick={() => handleSort('assignee_id')}
            >
              Assignee {sortBy === 'assignee_id' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-24" 
              onClick={() => handleSort('status')}
            >
              Status {sortBy === 'status' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-20" 
              onClick={() => handleSort('priority')}
            >
              Priority {sortBy === 'priority' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th 
              className="px-3 py-2 text-left cursor-pointer hover:bg-gray-200 w-32" 
              onClick={() => handleSort('due_date')}
            >
              Due Date {sortBy === 'due_date' && (sortDir === 'asc' ? '↑' : '↓')}
            </th>
            <th className="px-3 py-2 text-center w-40">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white text-gray-700">
          {tasks.map(task => (
            <tr key={task.id} className="hover:bg-gray-50">
              <td className="px-3 py-2 font-medium truncate" title={task.title}>{task.title}</td>
              <td className="px-3 py-2 max-w-xs" title={task.description || 'No description'}>
                <div className="overflow-hidden" style={{ 
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  maxHeight: '2.5rem'
                }}>
                  <p className="text-sm leading-tight">
                    {task.description || '-'}
                  </p>
                </div>
              </td>
              <td className="px-3 py-2 truncate">{getUserName(task.assignee_id)}</td>
              <td className="px-3 py-2">
                <StatusBadge status={task.status} />
              </td>
              <td className="px-3 py-2">
                <PriorityBadge priority={task.priority} />
              </td>
              <td className="px-3 py-2 text-xs">{formatDateTime(task.due_date)}</td>
              <td className="px-3 py-2 text-center">
                <div className="flex items-center justify-center gap-2">
                  <button 
                    className="inline-flex items-center gap-1 text-green-600 bg-green-50 border border-green-200 hover:bg-green-100 text-xs px-2 py-1 rounded transition"
                    onClick={() => onViewTask && onViewTask(task)}
                    title="View task details"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    View
                  </button>
                  <button 
                    className={`inline-flex items-center gap-1 text-blue-600 bg-blue-50 border border-blue-200 hover:bg-blue-100 text-xs px-2 py-1 rounded transition ${
                      canEdit(task) ? '' : 'opacity-50 pointer-events-none'
                    }`}
                    onClick={() => canEdit(task) && onEditTask(task)}
                    disabled={!canEdit(task)}
                    title="Edit task"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit
                  </button>
                  {canDelete() && (
                    <button 
                      className="inline-flex items-center gap-1 text-red-600 bg-red-50 border border-red-200 hover:bg-red-100 text-xs px-2 py-1 rounded transition"
                      onClick={() => onDeleteTask(task)}
                      title="Delete task"
                    >
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Delete
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
          {tasks.length === 0 && (
            <tr>
              <td colSpan="7" className="px-3 py-8 text-center text-gray-500">
                No tasks found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
