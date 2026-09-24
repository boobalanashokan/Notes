import { useEffect, useState } from 'react'
import { getTrackStats } from '../api'
import { useTrack } from '../TrackContext'

function Dashboard() {
  const { trackId, trackName, loading: tracksLoading } = useTrack()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (tracksLoading || !trackId) {
      setLoading(true)
      return
    }

    let ignore = false

    async function loadStats() {
      try {
        setLoading(true)
        const data = await getTrackStats(trackId)
        if (!ignore) {
          setStats(data)
          setError('')
        }
      } catch (err) {
        if (!ignore) {
          setStats(null)
          setError('Could not reach backend — is it running on port 8000?')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadStats()
    return () => {
      ignore = true
    }
  }, [trackId, tracksLoading])

  if (tracksLoading || !trackId || loading) {
    return <div className="page-shell"><div className="card"><p>Loading dashboard...</p></div></div>
  }

  if (error) {
    return <div className="page-shell"><div className="card error-box"><p>{error}</p></div></div>
  }

  const progressValue = Math.round(stats.percent_complete || 0)

  return (
    <div className="page-shell">
      <div className="card hero-card">
        <div className="hero-row">
          <div>
            <p className="eyebrow">{trackName || 'Track'} progress</p>
            <h1>{progressValue}% complete</h1>
          </div>
          <div className="big-pill">{stats.completed_topics}/{stats.total_topics} complete</div>
        </div>

        <div className="progress-bar" aria-label="Track completion progress">
          <div className="progress-fill" style={{ width: `${progressValue}%` }} />
        </div>
      </div>

      <div className="stats-grid">
        <div className="card small-card">
          <p className="stat-label">Total topics</p>
          <h2>{stats.total_topics}</h2>
        </div>
        <div className="card small-card">
          <p className="stat-label">Completed</p>
          <h2>{stats.completed_topics}</h2>
        </div>
        <div className="card small-card">
          <p className="stat-label">Remaining</p>
          <h2>{stats.remaining_topics}</h2>
        </div>
      </div>

      <div className="card">
        <h3>Progress by Area</h3>
        <div className="area-list">
          {stats.areas.map((area) => (
            <div key={area.area_name} className="area-row">
              <div className="area-header-row">
                <span>{area.area_name}</span>
                <span>{area.percent_complete}%</span>
              </div>
              <div className="progress-bar small" aria-label={`${area.area_name} progress`}>
                <div className="progress-fill" style={{ width: `${area.percent_complete}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
