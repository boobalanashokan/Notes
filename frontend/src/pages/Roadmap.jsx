import { useEffect, useMemo, useState } from 'react'
import { getTrack } from '../api'
import { useTrack } from '../TrackContext'

function Roadmap() {
  const { trackId, loading: tracksLoading } = useTrack()
  const [track, setTrack] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedArea, setSelectedArea] = useState('All')
  const [selectedStatus, setSelectedStatus] = useState('All')
  const [expandedAreas, setExpandedAreas] = useState({})

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
          if (data?.areas?.length) {
            setExpandedAreas({ [data.areas[0].id]: true })
          }
        }
      } catch (err) {
        if (!ignore) {
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

  const areaOptions = useMemo(() => {
    if (!track?.areas) return []
    return ['All', ...track.areas.map((area) => area.name)]
  }, [track])

  const filteredAreas = useMemo(() => {
    if (!track?.areas) return []

    return track.areas.filter((area) => {
      const areaMatches = selectedArea === 'All' || area.name === selectedArea
      const visibleTopics = area.topics.filter((topic) => {
        const statusMatches =
          selectedStatus === 'All' ||
          (selectedStatus === 'Done' && topic.done) ||
          (selectedStatus === 'Not Done' && !topic.done)
        return statusMatches
      })
      return areaMatches && visibleTopics.length > 0
    })
  }, [track, selectedArea, selectedStatus])

  const toggleArea = (areaId) => {
    setExpandedAreas((current) => ({
      ...current,
      [areaId]: !current[areaId],
    }))
  }

  if (loading) {
    return <div className="page-shell"><div className="card"><p>Loading roadmap...</p></div></div>
  }

  if (error) {
    return <div className="page-shell"><div className="card error-box"><p>{error}</p></div></div>
  }

  return (
    <div className="page-shell">
      <div className="card filter-card">
        <div className="filter-row">
          <label>
            <span>Area</span>
            <select value={selectedArea} onChange={(e) => setSelectedArea(e.target.value)}>
              {areaOptions.map((area) => (
                <option key={area} value={area}>{area}</option>
              ))}
            </select>
          </label>

          <label>
            <span>Status</span>
            <select value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
              <option value="All">All</option>
              <option value="Done">Done</option>
              <option value="Not Done">Not Done</option>
            </select>
          </label>
        </div>
      </div>

      <div className="area-stack">
        {filteredAreas.map((area) => {
          const isExpanded = expandedAreas[area.id] ?? false
          const visibleTopics = area.topics.filter((topic) => {
            return (
              selectedStatus === 'All' ||
              (selectedStatus === 'Done' && topic.done) ||
              (selectedStatus === 'Not Done' && !topic.done)
            )
          })

          return (
            <div key={area.id} className="card area-section">
              <button
                type="button"
                className="section-toggle"
                onClick={() => toggleArea(area.id)}
              >
                <span>{area.name}</span>
                <span>{isExpanded ? '−' : '+'}</span>
              </button>

              {isExpanded && (
                <div className="topics-list">
                  {visibleTopics.map((topic) => (
                    <div key={topic.id} className="topic-card">
                      <div className="topic-header-row">
                        <h4>{topic.name}</h4>
                        <div className={`status-badge ${topic.done ? 'done' : 'not-done'}`}>
                          {topic.done ? '✓ Done' : '○ Not done'}
                        </div>
                      </div>

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
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Roadmap
