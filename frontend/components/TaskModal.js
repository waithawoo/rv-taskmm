'use client'
import { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'

export default function TaskModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  task = null, 
  users = [],
  validationErrors = {} 
}) {
  const { user } = useAuth()
  const isAdmin = user?.role === 'admin'
  const isEditing = !!task
  const isMyTask = task && user?.id && Number(task.assignee_id) === Number(user.id)

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assignee_id: '',
    status: 'TODO',
    priority: 'LOW',
    due_date: ''
  })

  useEffect(() => {
    if (task) {
      let dueDateValue = ''
      if (task.due_date) {
        try {
          const date = new Date(task.due_date)
          if (!isNaN(date.getTime())) {
            dueDateValue = date.toISOString().slice(0, 16)
          }
        } catch (e) {
          console.error('Error parsing due_date:', e)
        }
      }
      
      setFormData({
        title: task.title || '',
        description: task.description || '',
        assignee_id: task.assignee_id || '',
        status: task.status || 'TODO',
        priority: task.priority || 'LOW',
        due_date: dueDateValue
      })
    } else {
      setFormData({
        title: '',
        description: '',
        assignee_id: users[0]?.id || '',
        status: 'TODO',
        priority: 'LOW',
        due_date: ''
      })
    }
  }, [task, users])

  useEffect(() => {
    if (!isOpen && !task) {
      setFormData({
        title: '',
        description: '',
        assignee_id: '',
        status: 'TODO',
        priority: 'LOW',
        due_date: ''
      })
    }
  }, [isOpen, task])

  const getFieldError = (fieldName) => {
    return validationErrors[fieldName] || null
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const submitData = {
      ...formData,
      assignee_id: formData.assignee_id === '' ? null : formData.assignee_id
    }
    
    onSubmit(submitData)
  }

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  if (!isOpen) return null

  // Permission
  const canEditTitle = isAdmin
  const canEditDescription = isAdmin
  const canEditAssignee = isAdmin
  const canEditPriority = isAdmin
  const canEditDueDate = isAdmin
  const canEditStatus = isAdmin || (isMyTask && isEditing)

  return (
    <div className="fixed inset-0 bg-transparent bg-opacity-20 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-white rounded shadow-lg p-6 w-full max-w-lg">
        <h2 className="text-lg font-bold mb-4">
          {isEditing ? 'Edit Task' : 'New Task'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-sm font-medium">Title</label>
            <input 
              type="text" 
              className={`w-full border px-2 py-1 rounded ${getFieldError('title') ? 'border-red-500' : ''}`}
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              disabled={!canEditTitle}
              required 
            />
            {getFieldError('title') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('title')}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium">Description</label>
            <textarea 
              className={`w-full border px-2 py-1 rounded ${getFieldError('description') ? 'border-red-500' : ''}`}
              rows="2"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              disabled={!canEditDescription}
            />
            {getFieldError('description') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('description')}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium">Assignee</label>
            <select 
              className={`w-full border px-2 py-1 rounded ${getFieldError('assignee_id') ? 'border-red-500' : ''}`}
              value={formData.assignee_id}
              onChange={(e) => handleChange('assignee_id', e.target.value)}
              disabled={!canEditAssignee}
            >
              <option value="">Unassigned</option>
              {users.map(u => (
                <option key={u.id} value={u.id}>{u.name}</option>
              ))}
            </select>
            {getFieldError('assignee_id') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('assignee_id')}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium">Status</label>
            <select 
              className={`w-full border px-2 py-1 rounded ${getFieldError('status') ? 'border-red-500' : ''}`}
              value={formData.status}
              onChange={(e) => handleChange('status', e.target.value)}
              disabled={!canEditStatus}
            >
              <option value="TODO">TODO</option>
              <option value="IN_PROGRESS">IN PROGRESS</option>
              <option value="DONE">DONE</option>
            </select>
            {getFieldError('status') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('status')}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium">Priority</label>
            <select 
              className={`w-full border px-2 py-1 rounded ${getFieldError('priority') ? 'border-red-500' : ''}`}
              value={formData.priority}
              onChange={(e) => handleChange('priority', e.target.value)}
              disabled={!canEditPriority}
            >
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
            {getFieldError('priority') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('priority')}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium">Due Date & Time</label>
            <input 
              type="datetime-local" 
              className={`w-full border px-2 py-1 rounded ${getFieldError('due_date') ? 'border-red-500' : ''}`}
              value={formData.due_date}
              onChange={(e) => handleChange('due_date', e.target.value)}
              disabled={!canEditDueDate}
            />
            {getFieldError('due_date') && (
              <p className="text-red-600 text-xs mt-1">{getFieldError('due_date')}</p>
            )}
          </div>
          
          <div className="flex justify-end gap-2 mt-4">
            <button 
              type="button" 
              onClick={onClose}
              className="px-3 py-1 rounded border border-gray-300 text-gray-600 hover:bg-gray-100"
            >
              Cancel
            </button>
            <button 
              type="submit"
              className="px-3 py-1 rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
