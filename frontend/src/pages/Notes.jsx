import { useEffect, useState } from 'react'
import { getTrack } from '../api'
import { useTrack } from '../TrackContext'

function Notes() {
  const { trackId, loading: tracksLoading } = useTrack()
  const [track, setTrack] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedTopics, setExpandedTopics] = useState({})

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

  const toggleTopic = (topicId) => {
    setExpandedTopics((current) => ({
      ...current,
      [topicId]: !current[topicId],
    }))
  }

  if (tracksLoading || !trackId || loading) {
    return <div className="page-shell"><div className="card"><p>Loading notes...</p></div></div>
  }

  if (error) {
    return <div className="page-shell"><div className="card error-box"><p>{error}</p></div></div>
  }

  return (
    <div className="page-shell notes-page">
      <div className="card page-header-card">
        <div className="page-heading">
          <div>
            <span className="page-kicker">Knowledge</span>
            <h2>Notes</h2>
          </div>
          <div className="page-header-metrics">
            <span className="page-metric-pill">{track?.areas?.length || 0} areas</span>
            <span className="page-metric-pill">{track?.areas?.reduce((count, area) => count + (area.topics?.length || 0), 0) || 0} topics</span>
          </div>
        </div>
        <p className="page-subtitle">Review the concepts, outcomes, and action items behind each topic in this track.</p>
      </div>

      <div className="area-stack">
        {track?.areas?.map((area) => (
          <div key={area.id} className="card area-section">
            <button type="button" className="section-toggle">
              <span>{area.name}</span>
              <span>•</span>
            </button>

            <div className="topics-list">
              {area.topics.map((topic) => {
                const isExpanded = !!expandedTopics[topic.id]
                return (
                  <div key={topic.id} className="topic-card">
                    <div className="topic-header-row">
                      <button
                        type="button"
                        className="topic-toggle-button"
                        onClick={() => toggleTopic(topic.id)}
                      >
                        <h4>{topic.name}</h4>
                      </button>
                      <div className={`status-badge ${topic.done ? 'done' : 'not-done'}`}>
                        {topic.done ? '✓ Done' : '○ Not done'}
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="detail-block">
                        <div className="topic-meta">
                          <span>Week {topic.week}</span>
                        </div>

                        <ul className="subtopic-list">
                          {topic.subtopics.map((subtopic) => (
                            <li key={subtopic}>{subtopic}</li>
                          ))}
                        </ul>

                        <div className="detail-block">
                          <strong>Learning outcome:</strong>
                          <p>{topic.learning_outcome}</p>
                        </div>

                        <div className="detail-block">
                          <strong>Project task:</strong>
                          <p>{topic.project_task}</p>
                        </div>

                        <div className="detail-block">
                          <strong>Full note content viewing coming soon</strong>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Notes
