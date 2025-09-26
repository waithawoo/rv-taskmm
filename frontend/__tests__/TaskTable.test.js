import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskTable from '../components/TaskTable'

const mockTasksFromAPI = [
  {
    id: 1,
    title: 'Implement user authentication',
    description: 'Add login and signup functionality',
    status: 'TODO',
    priority: 'HIGH',
    due_date: '2024-12-31T23:59:59',
    assignee_id: 1,
    creator_id: 1
  },
  {
    id: 2,
    title: 'Setup database',
    description: 'Configure PostgreSQL database',
    status: 'IN_PROGRESS',
    priority: 'MEDIUM',
    due_date: '2024-11-30T17:00:00',
    assignee_id: 2,
    creator_id: 1
  },
  {
    id: 3,
    title: 'Write documentation',
    description: 'Create API documentation',
    status: 'DONE',
    priority: 'LOW',
    due_date: null,
    assignee_id: null,
    creator_id: 2
  }
]

const mockUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'user' }
]

const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin' }

describe('Frontend Test - Rendering List with Mocked API', () => {
  const props = {
    tasks: mockTasksFromAPI,
    onSort: jest.fn(),
    sortBy: 'created_at',
    sortDir: 'desc',
    onViewTask: jest.fn(),
    onEditTask: jest.fn(),
    onDeleteTask: jest.fn(),
    users: mockUsers,
    user: mockUser
  }

  it('renders task list with mocked API data', () => {
    // Render the TaskTable component with mocked API data
    render(<TaskTable {...props} />)
    
    // Verify the table structure is rendered
    expect(screen.getByText('Title')).toBeInTheDocument()
    expect(screen.getByText('Description')).toBeInTheDocument()
    expect(screen.getByText('Status')).toBeInTheDocument()
    expect(screen.getByText('Priority')).toBeInTheDocument()
    expect(screen.getByText('Actions')).toBeInTheDocument()
    
    // Verify all mocked tasks from API are displayed
    expect(screen.getByText('Implement user authentication')).toBeInTheDocument()
    expect(screen.getByText('Setup database')).toBeInTheDocument()
    expect(screen.getByText('Write documentation')).toBeInTheDocument()
    
    // Verify task descriptions are rendered
    expect(screen.getByText('Add login and signup functionality')).toBeInTheDocument()
    expect(screen.getByText('Configure PostgreSQL database')).toBeInTheDocument()
    expect(screen.getByText('Create API documentation')).toBeInTheDocument()
    
    // Verify status badges from mocked data
    expect(screen.getByText('TODO')).toBeInTheDocument()
    expect(screen.getByText('IN PROGRESS')).toBeInTheDocument()
    expect(screen.getByText('DONE')).toBeInTheDocument()
    
    // Verify priority badges from mocked data
    expect(screen.getByText('HIGH')).toBeInTheDocument()
    expect(screen.getByText('MEDIUM')).toBeInTheDocument()
    expect(screen.getByText('LOW')).toBeInTheDocument()
    
    // Verify action buttons are rendered for each task
    const viewButtons = screen.getAllByText('View')
    const editButtons = screen.getAllByText('Edit')
    const deleteButtons = screen.getAllByText('Delete')
    
    expect(viewButtons).toHaveLength(3)
    expect(editButtons).toHaveLength(3)
    expect(deleteButtons).toHaveLength(3)
  })
})
