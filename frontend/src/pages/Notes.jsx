import React, { useEffect, useState } from 'react'
import { getFileViewerUrl, getTopicNote, getTrack } from '../api'
import { useTrack } from '../TrackContext'

function formatInlineMarkdown(text = '') {
  const regex = /(\*\*[^*]+\*\*|`[^`]+`)/g
  const parts = text.split(regex)

  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={`${part}-${index}`}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={`${part}-${index}`} style={{ background: '#1e293b', color: '#f8fafc', padding: '0.1rem 0.35rem', borderRadius: '4px' }}>{part.slice(1, -1)}</code>
    }
    return <span key={`${part}-${index}`}>{part}</span>
  })
}

function renderMarkdownContent(markdown = '') {
  const lines = (markdown || '').replace(/\r\n/g, '\n').split('\n')
  const nodes = []
  let index = 0

  while (index < lines.length) {
    const line = lines[index]

    if (!line.trim()) {
      index += 1
      continue
    }

    if (line.startsWith('```')) {
      const codeLines = []
      const language = line.replace(/^```/, '').trim()
      index += 1
      while (index < lines.length && !lines[index].startsWith('```')) {
        codeLines.push(lines[index])
        index += 1
      }
      const codeText = codeLines.join('\n')
      nodes.push(
        <pre key={`code-${nodes.length}`} style={{ background: '#0f172a', color: '#f8fafc', padding: '0.9rem', borderRadius: '8px', overflowX: 'auto', border: '1px solid #334155', margin: '0.8rem 0' }}>
          <code>{language ? `${language}\n${codeText}` : codeText}</code>
        </pre>,
      )
      index += 1
      continue
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.*)$/)
    if (headingMatch) {
      const level = headingMatch[1].length
      const text = headingMatch[2].trim()
      const styles = {
        margin: '0.8rem 0 0.5rem',
        color: '#ffffff',
        fontWeight: 700,
      }
      const headingTag = `h${Math.min(level, 6)}`
      nodes.push(
        React.createElement(
          headingTag,
          { key: `heading-${nodes.length}`, style: styles },
          formatInlineMarkdown(text),
        ),
      )
      index += 1
      continue
    }

    if (/^[-*]\s+/.test(line)) {
      const listItems = []
      while (index < lines.length && /^[-*]\s+/.test(lines[index])) {
        listItems.push(lines[index].replace(/^[-*]\s+/, '').trim())
        index += 1
      }
      nodes.push(
        <ul key={`list-${nodes.length}`} style={{ margin: '0.6rem 0', paddingLeft: '1.2rem', color: '#f8fafc' }}>
          {listItems.map((item, itemIndex) => (
            <li key={`${item}-${itemIndex}`} style={{ marginBottom: '0.25rem' }}>{formatInlineMarkdown(item)}</li>
          ))}
        </ul>,
      )
      continue
    }

    const paragraph = []
    while (
      index < lines.length &&
      lines[index].trim() &&
      !lines[index].startsWith('```') &&
      !/^#{1,6}\s+/.test(lines[index]) &&
      !/^[-*]\s+/.test(lines[index])
    ) {
      paragraph.push(lines[index].trim())
      index += 1
    }

    nodes.push(
      <p key={`para-${nodes.length}`} style={{ margin: '0.5rem 0', lineHeight: 1.7, color: '#ffffff' }}>
        {formatInlineMarkdown(paragraph.join(' '))}
      </p>,
    )
  }

  return nodes
}

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
                                <div
                                  style={{
                                    marginTop: '0.75rem',
                                    background: '#0f172a',
                                    color: '#ffffff',
                                    border: '1px solid #334155',
                                    borderRadius: '10px',
                                    padding: '1rem',
                                    overflowX: 'auto',
                                    boxShadow: 'inset 0 0 0 1px rgba(148, 163, 184, 0.18)',
                                  }}
                                >
                                  {renderMarkdownContent(note.content || 'No content saved in this note yet.')}
                                </div>

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
