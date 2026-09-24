import { useEffect, useMemo, useState } from 'react'
import { getTrackStats } from '../api'
import { useTrack } from '../TrackContext'

function Skills() {
  const { trackId, loading: tracksLoading } = useTrack()
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

  const sortedAreas = useMemo(() => {
    if (!stats?.areas) return []
    return [...stats.areas].sort((a, b) => (b.percent_complete || 0) - (a.percent_complete || 0))
  }, [stats])

  if (tracksLoading || !trackId || loading) {
    return <div className="page-shell"><div className="card"><p>Loading skills...</p></div></div>
  }

  if (error) {
    return <div className="page-shell"><div className="card error-box"><p>{error}</p></div></div>
  }

  return (
    <div className="page-shell">
      <div className="card">
        <h2>Skills</h2>
      </div>

      <div className="area-stack">
        {sortedAreas.map((area) => (
          <div key={area.area_name} className="card area-section">
            <div className="area-header-row">
              <span>{area.area_name}</span>
              <span>{area.percent_complete}%</span>
            </div>
            <div className="progress-bar" aria-label={`${area.area_name} progress`}>
              <div className="progress-fill" style={{ width: `${area.percent_complete}%` }} />
            </div>
            <p className="topic-meta">
              {area.completed_topics} / {area.total_topics} complete
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Skills
