'use client'

export default function Pagination({
  currentPage,
  totalPages,
  totalItems,
  pageSize,
  hasNext,
  onPageChange,
  onPageSizeChange
}) {
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1)
    }
  }

  const handleNext = () => {
    if (hasNext || currentPage < totalPages) {
      onPageChange(currentPage + 1)
    }
  }

  return (
    <div className="flex items-center justify-between mt-2">
      <div className="flex items-center gap-2">
        <label className="text-sm">Rows:</label>
        <select 
          className="border rounded px-1 py-0.5 text-sm"
          value={pageSize}
          onChange={(e) => onPageSizeChange(Number(e.target.value))}
        >
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="20">20</option>
        </select>
      </div>
      <div className="flex items-center gap-1">
        <button 
          onClick={handlePrevious}
          disabled={currentPage <= 1}
          className="px-2 py-1 border rounded text-xs bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Prev
        </button>
        <span className="text-sm px-2">
          Page {currentPage} {totalPages > 0 && `/ ${totalPages}`} ({totalItems} tasks)
        </span>
        <button 
          onClick={handleNext}
          disabled={!hasNext && currentPage >= totalPages}
          className="px-2 py-1 border rounded text-xs bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  )
}
