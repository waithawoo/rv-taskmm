'use client'
import { useEffect, useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import withAuth from '../../components/withAuth'
import request from '../../lib/api'
import FilterBar from '../../components/FilterBar'
import TaskTable from '../../components/TaskTable'
import TaskModal from '../../components/TaskModal'
import TaskDetailsModal from '../../components/TaskDetailsModal'
import Pagination from '../../components/Pagination'

function TasksPage() {
  const { user } = useAuth()
  
  const [tasks, setTasks] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  const [modalOpen, setModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [detailsModalOpen, setDetailsModalOpen] = useState(false)
  const [viewingTask, setViewingTask] = useState(null)
  const [notification, setNotification] = useState(null)
  const [validationErrors, setValidationErrors] = useState({})
  
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    priority: '',
    assignee: ''
  })
  const [sortBy, setSortBy] = useState('created_at')
  const [sortDir, setSortDir] = useState('desc')
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const [nextCursor, setNextCursor] = useState(null)
  const [hasNext, setHasNext] = useState(false)

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const queryParams = {
        limit: pageSize,
        search: filters.search,
        status: filters.status?.toLowerCase(),
        priority: filters.priority?.toLowerCase(),
        assignee_id: filters.assignee,
        sort: `${sortDir === 'desc' ? '-' : ''}${sortBy}`
      }

      if (currentPage > 1 && nextCursor) {
        queryParams.cursor = nextCursor
      }
      
      Object.keys(queryParams).forEach(key => {
        if (!queryParams[key]) delete queryParams[key]
      })
      
      const response = await request('/tasks', { qs: queryParams })
      
      if (response.success) {
        setTasks(response.data || [])
        setNextCursor(response.metadata?.next_cursor || null)
        setHasNext(response.metadata?.has_next || false)
        setTotalItems(response.metadata?.total || response.data?.length || 0)
      } else {
        setTasks(response.items || response || [])
        setTotalPages(response.totalPages || 1)
        setTotalItems(response.total || response.length || 0)
      }
    } catch (err) {
      setError(err.message)
      setTasks([])
    } finally {
      setLoading(false)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await request('/users/list')
      if (response.success) {
        setUsers(response.data || [])
      } else {
        setUsers(response || [])
      }
    } catch (err) {
      console.error('Failed to fetch users:', err)
      showNotification('Failed to load users: ' + err.message, 'error')
      setUsers([])
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [currentPage, pageSize, filters, sortBy, sortDir])

  useEffect(() => {
    fetchUsers()
  }, [user])

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }))
    setCurrentPage(1)
  }

  const handleClearFilters = () => {
    setFilters({ search: '', status: '', priority: '', assignee: '' })
    setCurrentPage(1)
  }

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortDir('asc')
    }
  }

  const handleAddTask = () => {
    setEditingTask(null)
    setValidationErrors({})
    setModalOpen(true)
  }

  const handleEditTask = (task) => {
    setEditingTask(task)
    setValidationErrors({})
    setModalOpen(true)
  }

  const handleViewTask = (task) => {
    setViewingTask(task)
    setDetailsModalOpen(true)
  }

  const handleCloseDetailsModal = () => {
    setDetailsModalOpen(false)
    setViewingTask(null)
  }

  const handleEditFromDetails = (task) => {
    setDetailsModalOpen(false)
    setViewingTask(null)
    setEditingTask(task)
    setValidationErrors({})
    setModalOpen(true)
  }

  const handleDeleteFromDetails = async (task) => {
    setDetailsModalOpen(false)
    setViewingTask(null)
    await handleDeleteTask(task)
  }

  const handleDeleteTask = async (task) => {
    if (!confirm(`Are you sure you want to delete "${task.title}"?`)) return
    
    try {
      await request(`/tasks/${task.id}`, { method: 'DELETE' })
      showNotification('Task deleted successfully', 'success')
      fetchTasks()
    } catch (err) {
      showNotification(err.message, 'error')
    }
  }

  const handleModalSubmit = async (formData) => {
    try {
      setValidationErrors({})
      
      if (editingTask) {
        await request(`/tasks/${editingTask.id}`, {
          method: 'PATCH',
          body: formData
        })
        showNotification('Task updated successfully', 'success')
      } else {
        await request('/tasks', {
          method: 'POST',
          body: formData
        })
        showNotification('Task created successfully', 'success')
      }
      setModalOpen(false)
      setEditingTask(null)
      fetchTasks()
    } catch (err) {
      if ((err.status === 400 || err.status === 422) && err.data && err.data.error_details && err.data.error_details.validationErrors) {
        const fieldErrors = {}
        err.data.error_details.validationErrors.forEach(error => {
          fieldErrors[error.field] = error.error
        })
        setValidationErrors(fieldErrors)
      } else {
        showNotification(err.message, 'error')
      }
    }
  }

  const handlePageSizeChange = (newSize) => {
    setPageSize(newSize)
    setCurrentPage(1)
  }

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  if (loading && tasks.length === 0) {
    return <div className="text-center py-8">Loading tasks...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {notification && (
          <div className={`w-full mb-4 px-4 py-2 rounded text-sm font-medium ${
            notification.type === 'success' ? 'bg-green-100 text-green-800' :
            notification.type === 'error' ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {notification.message}
          </div>
        )}
        
        {error && (
          <div className="w-full mb-4 px-4 py-2 rounded bg-red-100 text-red-800 text-sm font-medium">
            {error}
          </div>
        )}
        
        <div className="flex justify-between items-center mb-4">
          <div>
            <span className="font-bold text-lg">Task List</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">
              Hi, {user?.name || user?.email || 'User'} ({user?.role || 'user'})
            </span>
          </div>
        </div>
        
        <FilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          onClearFilters={handleClearFilters}
          onAddTask={handleAddTask}
          users={users}
          user={user}
        />
        
        {error && (
          <div className="bg-red-100 text-red-800 p-3 rounded mb-3">
            {error}
          </div>
        )}
        
        <TaskTable
          tasks={tasks}
          onSort={handleSort}
          sortBy={sortBy}
          sortDir={sortDir}
          onViewTask={handleViewTask}
          onEditTask={handleEditTask}
          onDeleteTask={handleDeleteTask}
          users={users}
          user={user}
        />
        
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          totalItems={totalItems}
          pageSize={pageSize}
          hasNext={hasNext}
          onPageChange={setCurrentPage}
          onPageSizeChange={handlePageSizeChange}
        />
        
        <TaskModal
          isOpen={modalOpen}
          onClose={() => {
            setModalOpen(false)
            setEditingTask(null)
            setValidationErrors({})
          }}
          onSubmit={handleModalSubmit}
          task={editingTask}
          users={users}
          validationErrors={validationErrors}
        />

        <TaskDetailsModal
          isOpen={detailsModalOpen}
          onClose={handleCloseDetailsModal}
          task={viewingTask}
          users={users}
          onEdit={handleEditFromDetails}
          onDelete={handleDeleteFromDetails}
        />
      </div>
    </div>
  )
}

export default withAuth(TasksPage)
