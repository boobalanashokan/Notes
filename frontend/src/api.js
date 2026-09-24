const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

async function readJsonResponse(response) {
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    return response.json()
  }

  const text = await response.text()
  return text ? JSON.parse(text) : null
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options)
  const payload = await readJsonResponse(response)

  if (!response.ok) {
    const detail = payload?.detail || payload?.error || `Request failed for ${url}: ${response.status} ${response.statusText}`
    const error = new Error(detail)
    error.savedFiles = payload?.saved_files || []
    throw error
  }

  return payload
}

export async function getTracks() {
  return requestJson(`${API_BASE}/tracks`)
}

export async function getTrackStats(trackId) {
  return requestJson(`${API_BASE}/tracks/${trackId}/stats`)
}

export async function getTrack(trackId) {
  return requestJson(`${API_BASE}/tracks/${trackId}`)
}

export async function uploadFiles(trackId, files) {
  const formData = new FormData()
  files.forEach((file) => {
    formData.append('files', file, file.name)
  })

  const response = await fetch(`${API_BASE}/tracks/${trackId}/upload`, {
    method: 'POST',
    body: formData,
  })

  const payload = await readJsonResponse(response)

  if (!response.ok) {
    const detail = payload?.detail || payload?.error || `Upload failed: ${response.status}`
    const error = new Error(detail)
    error.savedFiles = payload?.saved_files || []
    throw error
  }

  return payload
}

export async function getMappingOptions(trackId, areaId, topicId) {
  return requestJson(`${API_BASE}/tracks/${trackId}/areas/${areaId}/topics/${topicId}/mapping-options`)
}

export async function previewMapping(trackId, areaId, topicId, payload) {
  return requestJson(`${API_BASE}/tracks/${trackId}/areas/${areaId}/topics/${topicId}/preview`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}

export async function approveMapping(trackId, areaId, topicId, payload) {
  return requestJson(`${API_BASE}/tracks/${trackId}/areas/${areaId}/topics/${topicId}/approve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}

export { API_BASE }
