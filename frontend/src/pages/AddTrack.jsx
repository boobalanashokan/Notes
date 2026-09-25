import { useMemo, useState } from 'react'
import { API_BASE } from '../api'

const trackCreationPrompt = [
  'Generate a learning curriculum as a single JSON object for a study-tracker app, in EXACTLY this schema — no extra fields, no markdown formatting, no commentary, just the raw JSON:',
  '',
  '{',
  '  "id": "slug-version-of-track-name",',
  '  "name": "Display Name",',
  '  "areas": [',
  '    {',
  '      "id": "slug-version-of-area-name",',
  '      "name": "Display Name",',
  '      "topics": [',
  '        {',
  '          "id": "slug-version-of-topic-name",',
  '          "name": "Display Name",',
  '          "week": 1,',
  '          "type": "Learn",',
  '          "subtopics": ["short phrase", "short phrase"],',
  '          "learning_outcome": "One sentence describing what the learner should be able to explain or do after this topic.",',
  '          "project_task": "One concrete, hands-on task that proves this was learned.",',
  '          "depends_on": [],',
  '          "done": false',
  '        }',
  '      ]',
  '    }',
  '  ]',
  '}',
  '',
  'Rules:',
  '- All "id" fields (track, area, topic) must be lowercase, hyphenated, no special characters or spaces (e.g. "data-ingestion" not "Data Ingestion" or "data_ingestion").',
  '- "depends_on" contains topic ids from elsewhere in THIS SAME curriculum only, only when there\'s a real prerequisite relationship. Leave as [] if there\'s no dependency.',
  '- "week" should increase roughly in the order the learner should study, starting at 1.',
  '- "type" is one of: "Learn", "Build", "Review".',
  '- Keep subtopics as short phrases (3-6 words), not full sentences.',
  '- "done" is always false.',
  '- Output ONLY the JSON object, nothing else — no ```json fences, no explanation before or after.',
  '',
  'Now generate this curriculum for:',
  '',
  'Track name: [e.g. "Data Engineering"]',
  'Scope: [e.g. "Cover SQL fundamentals, data warehousing basics, ETL/ELT pipelines, Airflow orchestration, dbt, batch vs streaming, and a capstone project pattern. Assume the learner already knows Python and basic Linux from a prior MLOps track."]',
  'Target depth: [e.g. "~15-20 topics total across 5-6 areas, roughly 8 weeks of part-time study"]',
].join('\n')

function AddTrack() {
  const [jsonText, setJsonText] = useState('')
  const [parsedTrack, setParsedTrack] = useState(null)
  const [validationError, setValidationError] = useState('')
  const [submitError, setSubmitError] = useState('')
  const [successInfo, setSuccessInfo] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const summary = useMemo(() => {
    if (!parsedTrack || typeof parsedTrack !== 'object') {
      return null
    }

    const areas = Array.isArray(parsedTrack.areas) ? parsedTrack.areas : []
    const topicCount = areas.reduce((count, area) => count + (Array.isArray(area.topics) ? area.topics.length : 0), 0)

    return {
      trackName: parsedTrack.name || 'Unnamed track',
      areaCount: areas.length,
      topicCount,
    }
  }, [parsedTrack])

  const handleValidate = () => {
    setSubmitError('')
    setSuccessInfo(null)

    try {
      const parsed = JSON.parse(jsonText)

      if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
        throw new Error('The pasted value must be a single JSON object for one track.')
      }

      if (!parsed.name || typeof parsed.name !== 'string') {
        throw new Error('The top-level JSON object must include a string name.')
      }

      if (!parsed.areas || !Array.isArray(parsed.areas)) {
        throw new Error('The top-level JSON object must include an areas array.')
      }

      const validId = /^[a-z0-9-]+$/
      const validType = new Set(['Learn', 'Build', 'Review'])
      const allTopicIds = new Set()

      parsed.areas.forEach((area, areaIndex) => {
        if (!area || typeof area !== 'object') {
          throw new Error(`Area at index ${areaIndex} is invalid.`)
        }
        if (!area.id || !validId.test(area.id)) {
          throw new Error(`Area id at index ${areaIndex} must be lowercase and hyphenated.`)
        }
        if (!area.name || typeof area.name !== 'string') {
          throw new Error(`Area name at index ${areaIndex} is required.`)
        }
        if (!Array.isArray(area.topics)) {
          throw new Error(`Area "${area.name}" must include a topics array.`)
        }

        area.topics.forEach((topic, topicIndex) => {
          if (!topic || typeof topic !== 'object') {
            throw new Error(`Topic at area ${area.name} index ${topicIndex} is invalid.`)
          }
          if (!topic.id || !validId.test(topic.id)) {
            throw new Error(`Topic id at area ${area.name} index ${topicIndex} must be lowercase and hyphenated.`)
          }
          if (!topic.name || typeof topic.name !== 'string') {
            throw new Error(`Topic name at area ${area.name} index ${topicIndex} is required.`)
          }
          if (!Number.isInteger(topic.week) || topic.week < 1) {
            throw new Error(`Topic "${topic.name}" must have a week value of 1 or greater.`)
          }
          if (!validType.has(topic.type)) {
            throw new Error(`Topic "${topic.name}" has an invalid type. Use Learn, Build, or Review.`)
          }
          if (!Array.isArray(topic.subtopics) || topic.subtopics.some((value) => typeof value !== 'string')) {
            throw new Error(`Topic "${topic.name}" must include a string array for subtopics.`)
          }
          if (!topic.learning_outcome || typeof topic.learning_outcome !== 'string') {
            throw new Error(`Topic "${topic.name}" must include a learning outcome.`)
          }
          if (!topic.project_task || typeof topic.project_task !== 'string') {
            throw new Error(`Topic "${topic.name}" must include a project task.`)
          }
          if (!Array.isArray(topic.depends_on) || topic.depends_on.some((dep) => typeof dep !== 'string')) {
            throw new Error(`Topic "${topic.name}" must include a string array for depends_on.`)
          }
          if (typeof topic.done !== 'boolean') {
            throw new Error(`Topic "${topic.name}" must have a boolean done value.`)
          }
          if (topic.done !== false) {
            throw new Error(`Topic "${topic.name}" must be created with done set to false.`)
          }

          allTopicIds.add(topic.id)
        })
      })

      parsed.areas.forEach((area) => {
        area.topics.forEach((topic) => {
          const invalidDependencies = (topic.depends_on || []).filter((dep) => !allTopicIds.has(dep))
          if (invalidDependencies.length) {
            throw new Error(`Topic "${topic.name}" depends on unknown topic ids: ${invalidDependencies.join(', ')}`)
          }
        })
      })

      setParsedTrack(parsed)
      setValidationError('')
    } catch (err) {
      setParsedTrack(null)
      setValidationError(err instanceof Error ? err.message : 'Invalid JSON. Please paste a valid track object.')
    }
  }

  const handleCreateTrack = async () => {
    if (!parsedTrack) {
      setSubmitError('Please validate the JSON before creating the track.')
      return
    }

    setIsSubmitting(true)
    setSubmitError('')
    setSuccessInfo(null)

    try {
      const response = await fetch(`${API_BASE}/tracks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parsedTrack),
      })

      const payload = await response.json().catch(() => null)

      if (!response.ok) {
        const detail = payload?.detail ?? payload?.error ?? 'Request failed'
        const message = typeof detail === 'string' ? detail : JSON.stringify(detail, null, 2)
        throw new Error(message)
      }

      setSuccessInfo({
        commitSha: payload.commit_sha,
        savedFiles: payload.saved_files || [],
      })
      setValidationError('')
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Unable to create the track.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="page-shell track-json-page">
      <div className="card page-header-card">
        <div className="page-heading">
          <div>
            <span className="page-kicker">Create</span>
            <h2>Add Track</h2>
          </div>
          <div className="page-header-metrics">
            <span className="page-metric-pill">JSON workflow</span>
          </div>
        </div>
        <p className="page-subtitle">Add a new study track by validating the curriculum JSON before creating it in the app.</p>
      </div>

      <div className="card">
        <div className="track-json-note">
          Need help generating this JSON? Ask any AI assistant with the track-creation prompt template, then paste the result here.
        </div>
        <div className="track-json-template">{trackCreationPrompt}</div>
      </div>

      <div className="card">
        <label>
          <span>Paste a single track JSON object</span>
          <textarea
            value={jsonText}
            onChange={(event) => setJsonText(event.target.value)}
            placeholder={'{\n  "id": "mlops",\n  "name": "MLOps",\n  "areas": []\n}'}
            rows={20}
          />
        </label>

        <div className="track-json-actions">
          <button type="button" className="primary-button" onClick={handleValidate}>
            Validate
          </button>
          <button type="button" className="secondary-button" onClick={handleCreateTrack} disabled={!parsedTrack || isSubmitting}>
            {isSubmitting ? 'Creating...' : 'Create Track'}
          </button>
        </div>

        {validationError ? <div className="inline-error error-box">{validationError}</div> : null}
        {submitError ? <div className="inline-error error-box">{submitError}</div> : null}

        {summary ? (
          <div className="track-summary" style={{ marginTop: '1rem' }}>
            <div className="summary-box">
              <h4>Track name</h4>
              <strong>{summary.trackName}</strong>
            </div>
            <div className="summary-box">
              <h4>Areas</h4>
              <strong>{summary.areaCount}</strong>
            </div>
            <div className="summary-box">
              <h4>Topics</h4>
              <strong>{summary.topicCount}</strong>
            </div>
          </div>
        ) : null}

        {successInfo ? (
          <div className="success-box approve-success-box" style={{ marginTop: '1rem' }}>
            <h3>Track created successfully.</h3>
            <p>Commit SHA: {successInfo.commitSha}</p>
            <p>Saved files: {successInfo.savedFiles.join(', ') || 'None'}</p>
            <p>Please refresh the page or reselect the track switcher to see the new track in the app.</p>
          </div>
        ) : null}
      </div>
    </div>
  )
}

export default AddTrack
