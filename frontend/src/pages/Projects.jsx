import { useEffect, useMemo, useState } from 'react'
import { getTrack } from '../api'
import { useTrack } from '../TrackContext'

function Projects() {
  const { trackId, loading: tracksLoading } = useTrack()
  const [track, setTrack] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('All')

  useEffect(() => {
    if (tracksLoading || !trackId) {
      setLoading(true)
      return
    }

    let ignore = false

    async function loadTrack() {
      try {
        setLoading(true)
        const data = await getTrack(trackId)
        if (!ignore) {
          setTrack(data)
          setError('')
        }
      } catch (err) {
        if (!ignore) {
          setTrack(null)
          setError('Could not reach backend — is it running on port 8000?')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadTrack()
    return () => {
      ignore = true
    }
  }, [trackId, tracksLoading])

  const projects = useMemo(() => {
    if (!track?.areas) return []

    const items = []
    track.areas.forEach((area) => {
      area.topics.forEach((topic) => {
        if (topic.project_task && topic.project_task.trim()) {
          items.push({
            ...topic,
            areaName: area.name,
          })
        }
      })
    })

    return items.filter((topic) => {
      if (filter === 'Done') return topic.done
      if (filter === 'Not Done') return !topic.done
      return true
    })
  }, [track, filter])

  if (tracksLoading || !trackId || loading) {
    return <div className="page-shell"><div className="card"><p>Loading projects...</p></div></div>
  }

  if (error) {
    return <div className="page-shell"><div className="card error-box"><p>{error}</p></div></div>
  }

  return (
    <div className="page-shell">
      <div className="card page-header-card">
        <div className="page-heading">
          <div>
            <span className="page-kicker">Build</span>
            <h2>Projects</h2>
          </div>
          <div className="page-header-metrics">
            <span className="page-metric-pill">{projects.length} active tasks</span>
          </div>
        </div>
        <p className="page-subtitle">Turn every lesson into something practical with the project tasks linked to your current track.</p>
      </div>

      <div className="card filter-card">
        <div className="filter-row">
          <label className="filter-field">
            <span>Status</span>
            <select value={filter} onChange={(event) => setFilter(event.target.value)}>
              <option value="All">All</option>
              <option value="Done">Done</option>
              <option value="Not Done">Not Done</option>
            </select>
          </label>
        </div>
      </div>

      <div className="projects-grid">
        {projects.map((project) => (
          <div key={project.id} className="card small-card">
            <div className="topic-header-row">
              <h3>{project.name}</h3>
              <div className={`status-badge ${project.done ? 'done' : 'not-done'}`}>
                {project.done ? '✓ Done' : '○ Not done'}
              </div>
            </div>

            <p className="stat-label">{project.areaName}</p>
            <p>{project.project_task}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Projects
