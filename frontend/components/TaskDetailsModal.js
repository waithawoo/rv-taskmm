'use client'
import { useAuth } from '../hooks/useAuth'
import { StatusBadge, PriorityBadge } from './Badges'

export default function TaskDetailsModal({ 
  isOpen, 
  onClose, 
  task,
  users = [],
  onEdit,
  onDelete 
}) {
  const { user } = useAuth()
  
  if (!isOpen || !task) return null

  const isAdmin = user?.role === 'admin'
  const isMyTask = user?.id && Number(task.assignee_id) === Number(user.id)
  const canEdit = isAdmin || isMyTask
  const canDelete = isAdmin

  const assignedUser = users.find(u => u.id === task.assignee_id)

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set'
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) return 'Invalid date'
      return date.toLocaleString()
    } catch (e) {
      return 'Invalid date'
    }
  }

  return (
    <div className="fixed inset-0 bg-transparent bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Task Details</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Title Section */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Title</label>
            <h3 className="text-xl font-semibold text-gray-900">{task.title}</h3>
          </div>

          {/* Description */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <div className="bg-gray-50 rounded-lg p-4 min-h-[100px]">
              <p className="text-gray-700 whitespace-pre-wrap">
                {task.description || 'No description provided'}
              </p>
            </div>
          </div>

          {/* Status and Priority */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <StatusBadge status={task.status} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <PriorityBadge priority={task.priority} />
            </div>
          </div>

          {/* Assignee and Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Assignee</label>
              <div className="flex items-center">
                {assignedUser ? (
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-medium text-sm">
                      {assignedUser.name.charAt(0).toUpperCase()}
                    </div>
                    <span className="ml-3 text-gray-900">{assignedUser.name}</span>
                  </div>
                ) : (
                  <span className="text-gray-500 italic">Unassigned</span>
                )}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
              <p className="text-gray-900">{formatDate(task.due_date)}</p>
            </div>
          </div>

          {/* other dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Created At</label>
              <p className="text-gray-600 text-sm">{formatDate(task.created_at)}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Last Updated</label>
              <p className="text-gray-600 text-sm">{formatDate(task.updated_at)}</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex gap-3">
            <button 
              onClick={onClose}
              className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors"
            >
              Close
            </button>
            {canEdit && (
              <button 
                onClick={() => onEdit(task)}
                className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit
              </button>
            )}
            {canDelete && (
              <button 
                onClick={() => onDelete(task)}
                className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
