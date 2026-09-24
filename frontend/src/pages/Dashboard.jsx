import { useEffect, useState } from 'react'
import { getTrack, getTrackStats } from '../api'
import { useTrack } from '../TrackContext'

function Dashboard() {
  const { trackId, trackName, loading: tracksLoading } = useTrack()
  const [stats, setStats] = useState(null)
  const [track, setTrack] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (tracksLoading || !trackId) {
      setLoading(true)
      return
    }

    let ignore = false

    async function loadDashboardData() {
      try {
        setLoading(true)
        const [statsData, trackData] = await Promise.all([
          getTrackStats(trackId),
          getTrack(trackId),
        ])

        if (!ignore) {
          setStats(statsData)
          setTrack(trackData)
          setError('')
        }
      } catch (err) {
        if (!ignore) {
          setStats(null)
          setTrack(null)
          setError('Could not reach backend — is it running on port 8000?')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadDashboardData()
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
  const topicList = track?.areas?.flatMap((area) => area.topics.map((topic) => ({ ...topic, area_name: area.name }))) || []
  const weeksInTracker = topicList.length ? Math.max(...topicList.map((topic) => Number(topic.week) || 0)) : 0
  const nextTopic = topicList.find((topic) => !topic.done) || null
  const levelValue = Math.max(1, Math.min(99, Math.floor((stats.completed_topics / Math.max(stats.total_topics, 1)) * 100 / 12) + 1))

  const nextUpBadge = stats.remaining_topics === 0 ? 'Completed' : 'Next milestone'
  const nextUpTitle = nextTopic
    ? nextTopic.name
    : stats.remaining_topics === 0
      ? 'Track complete'
      : 'No topics available yet'
  const nextUpCopy = nextTopic
    ? `${nextTopic.area_name} · Week ${nextTopic.week}`
    : stats.remaining_topics === 0
      ? 'Everything in this track is complete.'
      : 'Start your learning journey by adding your first topic.'

  return (
    <div className="dashboard-layout">
      <div className="main-column">
        <section className="panel hero-panel">
          <div className="hero-copy">
            <p className="eyebrow">{(trackName || 'MLOps').toUpperCase()} TRACK</p>
            <div className="hero-badges">
              <span className="fun-badge level-badge">✨ Level {levelValue}</span>
              <span className="fun-badge streak-badge">⏱ {weeksInTracker} weeks in track</span>
            </div>
            <h1>
              Keep going,<br />
              <span className="gradient-text">you&apos;re making progress</span>
            </h1>
            <p className="hero-subtitle">Small steps every day build big skills. You&apos;ve got this.</p>
            <div className="quick-pills" aria-label="Learning focus options">
              <span className="focus-pill">{stats.completed_topics} complete</span>
              <span className="focus-pill">{stats.remaining_topics} left</span>
              <span className="focus-pill">{progressValue}% pace</span>
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
          <div className="panel-badge">{nextUpBadge}</div>
          <div className="sidebar-title-row">
            <span className="sidebar-symbol">◐</span>
            <h3>Next up</h3>
          </div>
          <div className="landscape-card">
            <div className="moon" />
            <div className="mountains mountains-back" />
            <div className="mountains mountains-front" />
          </div>
          <p>{nextUpTitle}</p>
          <p className="sidebar-copy">{nextUpCopy}</p>
          <button className="secondary-cta" type="button">{stats.remaining_topics === 0 ? 'Review roadmap' : 'Go to Roadmap'}</button>
        </section>

        <section className="panel weekly-panel">
          <div className="sidebar-title-row weekly-row">
            <span className="sidebar-symbol">◫</span>
            <h3>Track momentum</h3>
          </div>

          <div className="momentum-grid">
            <div className="momentum-item">
              <span className="momentum-label">Weeks in tracker</span>
              <strong>{weeksInTracker}</strong>
            </div>
            <div className="momentum-item">
              <span className="momentum-label">Completed</span>
              <strong>{stats.completed_topics}</strong>
            </div>
            <div className="momentum-item full-width">
              <span className="momentum-label">Current focus</span>
              <strong>{nextTopic ? nextTopic.name : 'No active topic'}</strong>
            </div>
          </div>
        </section>
      </aside>
    </div>
  )
}

export default Dashboard
