import { useEffect, useState } from 'react'
import { API_BASE, getFileViewerUrl, getTopicNote, getTrack } from '../api'
import { useTrack } from '../TrackContext'

function Notes() {
  const { trackId, loading: tracksLoading } = useTrack()
  const [track, setTrack] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedTopics, setExpandedTopics] = useState({})
  const [topicNotes, setTopicNotes] = useState({})
  const [noteLoading, setNoteLoading] = useState({})

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

  const fetchTopicNote = async (areaId, topicId) => {
    if (!trackId || !areaId || !topicId || topicNotes[topicId]) {
      return
    }

    setNoteLoading((current) => ({ ...current, [topicId]: true }))
    try {
      const payload = await getTopicNote(trackId, areaId, topicId)
      setTopicNotes((current) => ({
        ...current,
        [topicId]: payload,
      }))
    } catch (err) {
      setTopicNotes((current) => ({
        ...current,
        [topicId]: {
          target_path: '',
          file_exists: false,
          content: '',
          error: err.message || 'Could not load this topic note.',
        },
      }))
    } finally {
      setNoteLoading((current) => ({ ...current, [topicId]: false }))
    }
  }

  const toggleTopic = async (areaId, topicId) => {
    const nextExpanded = !expandedTopics[topicId]
    setExpandedTopics((current) => ({
      ...current,
      [topicId]: nextExpanded,
    }))

    if (nextExpanded) {
      await fetchTopicNote(areaId, topicId)
    }
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
                        onClick={() => toggleTopic(area.id, topic.id)}
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
                          <strong>Saved note</strong>
                          {noteLoading[topic.id] ? (
                            <p>Loading note...</p>
                          ) : (() => {
                            const note = topicNotes[topic.id]
                            if (note?.error) {
                              return <p>{note.error}</p>
                            }
                            if (!note?.file_exists) {
                              return <p>No note has been saved for this topic yet.</p>
                            }
                            return (
                              <>
                                <pre style={{ whiteSpace: 'pre-wrap', marginTop: '0.5rem', background: '#f5f7fb', padding: '0.75rem', borderRadius: '8px' }}>
                                  {note.content || 'No content saved in this note yet.'}
                                </pre>

                                {Array.isArray(note.source_files) && note.source_files.length > 0 && (
                                  <div style={{ marginTop: '1rem' }}>
                                    <strong>Source files</strong>
                                    <div style={{ display: 'grid', gap: '1rem', marginTop: '0.75rem' }}>
                                      {note.source_files.map((sourcePath) => {
                                        const fileName = sourcePath.split('/').pop() || sourcePath
                                        const extension = (fileName.split('.').pop() || '').toLowerCase()
                                        const viewerUrl = getFileViewerUrl(sourcePath)

                                        if (['pdf'].includes(extension)) {
                                          return (
                                            <div key={sourcePath}>
                                              <p style={{ marginBottom: '0.5rem' }}>{fileName}</p>
                                              <iframe
                                                src={viewerUrl}
                                                title={fileName}
                                                style={{ width: '100%', minHeight: '560px', border: '1px solid #dfe3ea', borderRadius: '8px', background: '#fff' }}
                                              />
                                            </div>
                                          )
                                        }

                                        if (['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(extension)) {
                                          return (
                                            <div key={sourcePath}>
                                              <p style={{ marginBottom: '0.5rem' }}>{fileName}</p>
                                              <img
                                                src={viewerUrl}
                                                alt={fileName}
                                                style={{ maxWidth: '100%', borderRadius: '8px', border: '1px solid #dfe3ea' }}
                                              />
                                            </div>
                                          )
                                        }

                                        return (
                                          <a key={sourcePath} href={viewerUrl} target="_blank" rel="noreferrer" style={{ display: 'inline-block', marginTop: '0.25rem' }}>
                                            Open {fileName}
                                          </a>
                                        )
                                      })}
                                    </div>
                                  </div>
                                )}
                              </>
                            )
                          })()}
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
