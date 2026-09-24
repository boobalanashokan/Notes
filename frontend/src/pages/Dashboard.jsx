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
  const weeklyProgress = [0, 0, 0, 0, 0, 0, 0]

  return (
    <div className="dashboard-layout">
      <div className="main-column">
        <section className="panel hero-panel">
          <div className="hero-copy">
            <p className="eyebrow">{(trackName || 'MLOps').toUpperCase()} TRACK</p>
            <div className="hero-badges">
              <span className="fun-badge level-badge">✨ Level 3</span>
              <span className="fun-badge streak-badge">🔥 12-day streak</span>
            </div>
            <h1>
              Keep going,<br />
              <span className="gradient-text">you&apos;re making progress</span>
            </h1>
            <p className="hero-subtitle">Small steps every day build big skills. You&apos;ve got this.</p>
            <div className="quick-pills" aria-label="Learning focus options">
              <span className="focus-pill">Deep work</span>
              <span className="focus-pill">Practice</span>
              <span className="focus-pill">Review</span>
            </div>
            <button className="primary-cta" type="button">
              <span className="cta-icon">▶</span>
              Continue learning
              <span className="cta-arrow">→</span>
            </button>
          </div>

          <div className="hero-visual">
            <div
              className="progress-ring"
              style={{
                background: `conic-gradient(#5ea6ff 0 ${progressValue}%, rgba(148, 163, 184, 0.18) ${progressValue}% 100%)`,
              }}
            >
              <div className="ring-inner">
                <strong>{progressValue}%</strong>
                <span>{stats.completed_topics} / {stats.total_topics} topics</span>
              </div>
            </div>

            <div className="mini-tip">
              <span className="mini-tip-icon">✦</span>
              <div>
                <strong>Learn today.</strong>
                <span>Build what&apos;s next.</span>
              </div>
            </div>
          </div>
        </section>

        <div className="stats-grid">
          <div className="panel stat-card total-card">
            <div className="stat-header">
              <span className="stat-icon">◫</span>
              <span className="stat-chevron">›</span>
            </div>
            <div className="stat-body">
              <div className="stat-label">Total topics</div>
              <div className="stat-value">{stats.total_topics}</div>
            </div>
          </div>

          <div className="panel stat-card completed-card">
            <div className="stat-header">
              <span className="stat-icon">✓</span>
              <span className="stat-chevron">›</span>
            </div>
            <div className="stat-body">
              <div className="stat-label">Completed</div>
              <div className="stat-value">{stats.completed_topics}</div>
            </div>
          </div>

          <div className="panel stat-card remaining-card">
            <div className="stat-header">
              <span className="stat-icon">◌</span>
              <span className="stat-chevron">›</span>
            </div>
            <div className="stat-body">
              <div className="stat-label">Remaining</div>
              <div className="stat-value">{stats.remaining_topics}</div>
            </div>
          </div>
        </div>

        <section className="panel area-panel">
          <h3>Progress by Area</h3>
          <div className="area-list">
            {stats.areas.map((area) => (
              <div key={area.area_name} className="area-row">
                <div className="area-header-row">
                  <span className="area-name-row">
                    <span className="area-dot" />
                    {area.area_name}
                  </span>
                  <span className="area-number-value">{area.percent_complete}%</span>
                </div>
                <div className="progress-bar small" aria-label={`${area.area_name} progress`}>
                  <div className="progress-fill" style={{ width: `${area.percent_complete}%` }} />
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <aside className="sidebar-column">
        <section className="panel nextup-panel">
          <div className="panel-badge">Recommended</div>
          <div className="sidebar-title-row">
            <span className="sidebar-symbol">◐</span>
            <h3>Next up</h3>
          </div>
          <div className="landscape-card">
            <div className="moon" />
            <div className="mountains mountains-back" />
            <div className="mountains mountains-front" />
          </div>
          <p>No topics available yet</p>
          <p className="sidebar-copy">Start your MLOps journey by exploring your first topic.</p>
          <button className="secondary-cta" type="button">Go to Roadmap</button>
        </section>

        <section className="panel weekly-panel">
          <div className="sidebar-title-row weekly-row">
            <span className="sidebar-symbol">◫</span>
            <h3>Weekly Consistency</h3>
            <span className="week-streak">0 day streak</span>
          </div>

          <div className="week-grid">
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, index) => (
              <div key={day} className="week-day">
                <div className={`day-dot ${weeklyProgress[index] ? 'filled' : ''}`} aria-label={`${day} progress`} />
                <span>{day}</span>
              </div>
            ))}
          </div>

          <div className="consistency-footer">
            <span className="consistency-icon">◎</span>
            <span>Consistency compounds. Show up this week!</span>
          </div>
        </section>
      </aside>
    </div>
  )
}

export default Dashboard
