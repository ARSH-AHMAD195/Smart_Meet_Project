export function formatDate(dateTimeStr) {
  const date = new Date(dateTimeStr)

  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}

export function formatTime(dateTimeStr) {
  const date = new Date(dateTimeStr)

  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  })
}

export function formatActionItems(rawItems = []) {
  return rawItems.map(item => ({
    id: item.id,
    task: item.task,
    assignee_name: item.assignee?.username || "Unassigned",
    due_date: formatDate(item.due_date),
  }))
}