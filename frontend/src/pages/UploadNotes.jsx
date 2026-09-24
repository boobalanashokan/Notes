import { useEffect, useState } from 'react'
import {
  approveMapping,
  getMappingOptions,
  getTrack,
  previewMapping,
  uploadFiles,
} from '../api'
import { useTrack } from '../TrackContext'

const VALID_EXTENSIONS = new Set(['.pdf', '.png', '.jpg', '.jpeg'])

function getFileExtension(filename) {
  const lower = (filename || '').toLowerCase()
  const index = lower.lastIndexOf('.')
  return index >= 0 ? lower.slice(index) : ''
}

function createMapping() {
  return {
    id: `mapping-${Math.random().toString(36).slice(2, 9)}`,
    areaId: '',
    topicId: '',
    status: 'Learning',
    noteText: '',
    selectedSubtopics: [],
    validSubtopics: [],
    preview: null,
    mode: 'append',
    previewLoading: false,
    approveLoading: false,
    approved: false,
    previewError: '',
    approveError: '',
    approveResult: null,
  }
}

function createFileEntry(file) {
  return {
    id: `file-${Math.random().toString(36).slice(2, 9)}`,
    name: file.name,
    savedPath: '',
    mappings: [createMapping()],
  }
}

function UploadNotes() {
  const { trackId, loading: tracksLoading } = useTrack()
  const [track, setTrack] = useState(null)
  const [selectedFiles, setSelectedFiles] = useState([])
  const [dragActive, setDragActive] = useState(false)
  const [uploadLoading, setUploadLoading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [uploadResult, setUploadResult] = useState(null)
  const [uploadedFileEntries, setUploadedFileEntries] = useState([])

  useEffect(() => {
    if (tracksLoading || !trackId) {
      return
    }

    let ignore = false

    async function loadTrack() {
      try {
        const data = await getTrack(trackId)
        if (!ignore) {
          setTrack(data)
        }
      } catch (err) {
        if (!ignore) {
          setTrack(null)
        }
      }
    }

    loadTrack()
    return () => {
      ignore = true
    }
  }, [trackId, tracksLoading])

  const areaOptions = track?.areas || []

  const addFiles = (incomingFiles) => {
    const nextFiles = Array.from(incomingFiles || [])
    const invalid = nextFiles.filter((file) => !VALID_EXTENSIONS.has(getFileExtension(file.name)))

    if (invalid.length > 0) {
      setUploadError(
        `The following files were skipped because they are not allowed: ${invalid
          .map((file) => file.name)
          .join(', ')}`,
      )
    }

    const validFiles = nextFiles.filter((file) => VALID_EXTENSIONS.has(getFileExtension(file.name)))
    if (validFiles.length === 0) {
      return
    }

    setSelectedFiles((current) => [...current, ...validFiles])
    setUploadError('')
  }

  const updateUploadedFile = (fileId, updater) => {
    setUploadedFileEntries((current) =>
      current.map((file) => (file.id === fileId ? updater(file) : file)),
    )
  }

  const updateMapping = (fileId, mappingId, updates) => {
    updateUploadedFile(fileId, (file) => ({
      ...file,
      mappings: file.mappings.map((mapping) =>
        mapping.id === mappingId ? { ...mapping, ...updates } : mapping,
      ),
    }))
  }

  const addAnotherMapping = (fileId) => {
    updateUploadedFile(fileId, (file) => ({
      ...file,
      mappings: [...file.mappings, createMapping()],
    }))
  }

  const handleAreaChange = (fileId, mappingId, areaId) => {
    updateMapping(fileId, mappingId, {
      areaId,
      topicId: '',
      validSubtopics: [],
      selectedSubtopics: [],
      preview: null,
      mode: 'append',
      approved: false,
      previewError: '',
      approveError: '',
      approveResult: null,
    })
  }

  const handleTopicChange = (fileId, mappingId, topicId) => {
    updateMapping(fileId, mappingId, {
      topicId,
      validSubtopics: [],
      selectedSubtopics: [],
      preview: null,
      mode: 'append',
      approved: false,
      previewError: '',
      approveError: '',
      approveResult: null,
    })
  }

  const loadValidSubtopics = async (fileId, mappingId, areaId, topicId) => {
    if (!areaId || !topicId) {
      updateMapping(fileId, mappingId, {
        validSubtopics: [],
        selectedSubtopics: [],
      })
      return
    }

    updateMapping(fileId, mappingId, {
      validSubtopics: [],
      selectedSubtopics: [],
      preview: null,
      previewError: '',
      approveError: '',
      approveResult: null,
      approved: false,
    })

    try {
      const data = await getMappingOptions(trackId, areaId, topicId)
      updateMapping(fileId, mappingId, {
        validSubtopics: data?.valid_subtopics || [],
      })
    } catch (err) {
      updateMapping(fileId, mappingId, {
        validSubtopics: [],
        previewError: err.message || 'Unable to load valid subtopics.',
      })
    }
  }

  const toggleSubtopic = (fileId, mappingId, subtopic) => {
    updateUploadedFile(fileId, (file) => ({
      ...file,
      mappings: file.mappings.map((mapping) => {
        if (mapping.id !== mappingId) {
          return mapping
        }

        const selected = mapping.selectedSubtopics.includes(subtopic)
        return {
          ...mapping,
          selectedSubtopics: selected
            ? mapping.selectedSubtopics.filter((item) => item !== subtopic)
            : [...mapping.selectedSubtopics, subtopic],
        }
      }),
    }))
  }

  const handleUpload = async () => {
    if (!selectedFiles.length) {
      setUploadError('Choose at least one valid file before continuing.')
      return
    }

    setUploadLoading(true)
    setUploadError('')
    setUploadResult(null)

    try {
      const result = await uploadFiles(trackId, selectedFiles)
      const savedFiles = Array.isArray(result?.saved_files) ? result.saved_files : []

      const nextEntries = selectedFiles.map((file, index) => {
        const exactSavedPath = savedFiles[index] || ''

        return {
          id: `file-${index}-${Math.random().toString(36).slice(2, 8)}`,
          name: file.name,
          savedPath: exactSavedPath,
          mappings: [createMapping()],
        }
      })

      setUploadResult(result)
      setUploadedFileEntries(nextEntries)
      setSelectedFiles([])
      setUploadLoading(false)
    } catch (err) {
      setUploadResult({ saved_files: err.savedFiles || [], commit_sha: null })
      setUploadError(err.message || 'Upload failed.')
      setUploadLoading(false)
    }
  }

  const handlePreview = async (fileId, mappingId) => {
    const file = uploadedFileEntries.find((entry) => entry.id === fileId)
    const mapping = file?.mappings.find((item) => item.id === mappingId)

    if (!file || !mapping || !mapping.areaId || !mapping.topicId) {
      updateMapping(fileId, mappingId, {
        previewError: 'Choose both area and topic before previewing.',
      })
      return
    }

    updateMapping(fileId, mappingId, {
      previewLoading: true,
      previewError: '',
      approveError: '',
      approved: false,
      approveResult: null,
    })

    try {
      const payload = {
        status: mapping.status,
        source_files: file.savedPath ? [file.savedPath] : [],
        subtopics: mapping.selectedSubtopics,
        note_text: mapping.noteText,
      }
      const result = await previewMapping(trackId, mapping.areaId, mapping.topicId, payload)
      updateMapping(fileId, mappingId, {
        preview: result,
        mode: result.file_exists ? 'append' : 'append',
        previewLoading: false,
        approveError: '',
      })
    } catch (err) {
      updateMapping(fileId, mappingId, {
        previewLoading: false,
        previewError: err.message || 'Preview failed.',
      })
    }
  }

  const handleApprove = async (fileId, mappingId) => {
    const file = uploadedFileEntries.find((entry) => entry.id === fileId)
    const mapping = file?.mappings.find((item) => item.id === mappingId)

    if (!file || !mapping || !mapping.preview) {
      updateMapping(fileId, mappingId, {
        approveError: 'Preview a mapping before approving it.',
      })
      return
    }

    if (mapping.preview.file_exists && !mapping.mode) {
      updateMapping(fileId, mappingId, {
        approveError: 'Select Append or Overwrite before approving an existing file.',
      })
      return
    }

    updateMapping(fileId, mappingId, {
      approveLoading: true,
      approveError: '',
    })

    try {
      const payload = {
        status: mapping.status,
        source_files: file.savedPath ? [file.savedPath] : [],
        subtopics: mapping.selectedSubtopics,
        note_text: mapping.noteText,
        ...(mapping.preview.file_exists ? { mode: mapping.mode } : {}),
      }

      const result = await approveMapping(trackId, mapping.areaId, mapping.topicId, payload)
      updateMapping(fileId, mappingId, {
        approveLoading: false,
        approveResult: result,
        approveError: '',
        approved: true,
      })
    } catch (err) {
      updateMapping(fileId, mappingId, {
        approveLoading: false,
        approveError: err.message || 'Approval failed.',
        approveResult: {
          saved_files: err.savedFiles || [],
        },
      })
    }
  }

  const selectedAreaTopics = (areaId) => {
    const area = areaOptions.find((item) => item.id === areaId)
    return area?.topics || []
  }

  const onDragOver = (event) => {
    event.preventDefault()
    setDragActive(true)
  }

  const onDragLeave = (event) => {
    event.preventDefault()
    setDragActive(false)
  }

  const onDrop = (event) => {
    event.preventDefault()
    setDragActive(false)
    addFiles(event.dataTransfer.files)
  }

  if (tracksLoading || !trackId) {
    return <div className="page-shell"><div className="card"><p>Loading upload page...</p></div></div>
  }

  return (
    <div className="page-shell">
      <div className="card page-header-card">
        <div className="page-heading">
          <div>
            <span className="page-kicker">Import</span>
            <h2>Upload Notes</h2>
          </div>
          <div className="page-header-metrics">
            <span className="page-metric-pill">{selectedFiles.length} selected</span>
          </div>
        </div>
        <p className="page-subtitle">Add study notes, map them to the right topic, and approve them into your learning track.</p>
      </div>

      <div className="card">
        <div
          className={`upload-dropzone ${dragActive ? 'drag-active' : ''}`}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
        >
          <input
            id="upload-notes-input"
            type="file"
            multiple
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={(event) => addFiles(event.target.files)}
            style={{ display: 'none' }}
          />
          <label htmlFor="upload-notes-input" className="upload-label">
            <span className="upload-drop-title">Drag and drop files here</span>
            <span className="upload-drop-subtitle">or click to browse (.pdf, .png, .jpg, .jpeg)</span>
          </label>
        </div>

        {selectedFiles.length > 0 && (
          <div className="selection-panel">
            <h3>Selected files</h3>
            <ul className="file-list">
              {selectedFiles.map((file) => (
                <li key={`${file.name}-${file.size}`}>
                  {file.name}
                </li>
              ))}
            </ul>
            <button
              type="button"
              className="primary-button"
              onClick={handleUpload}
              disabled={uploadLoading}
            >
              {uploadLoading ? 'Uploading...' : 'Continue'}
            </button>
          </div>
        )}

        {uploadError && (
          <div className="card error-box upload-error-box">
            <p>{uploadError}</p>
            {uploadResult?.saved_files?.length ? (
              <div className="saved-files-list">
                <strong>Saved locally:</strong>
                <ul>
                  {uploadResult.saved_files.map((path) => (
                    <li key={path}>{path}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        )}

        {uploadResult && !uploadError && (
          <div className="card success-box">
            <h3>Upload complete</h3>
            {uploadResult.commit_sha && <p>Commit SHA: {uploadResult.commit_sha}</p>}
            <div className="saved-files-list">
              <strong>Saved files:</strong>
              <ul>
                {uploadResult.saved_files.map((path) => (
                  <li key={path}>{path}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {uploadedFileEntries.length > 0 && (
        <div className="uploaded-files-panel">
          {uploadedFileEntries.map((file) => (
            <div key={file.id} className={`card mapping-file-card ${file.mappings.some((m) => m.approved) ? 'approved-file-card' : ''}`}>
              <div className="mapping-header-row">
                <h3>{file.name}</h3>
                {file.savedPath && <span className="saved-path-label">Stored as: {file.savedPath}</span>}
              </div>

              {file.mappings.map((mapping) => (
                <div key={mapping.id} className={`mapping-card ${mapping.approved ? 'mapping-card-approved' : ''}`}>
                  {mapping.approved && (
                    <div className="approved-banner">✓ Approved</div>
                  )}

                  <div className="form-grid">
                    <label>
                      <span>Area</span>
                      <select
                        value={mapping.areaId}
                        onChange={(event) => handleAreaChange(file.id, mapping.id, event.target.value)}
                      >
                        <option value="">Select area</option>
                        {areaOptions.map((area) => (
                          <option key={area.id} value={area.id}>
                            {area.name}
                          </option>
                        ))}
                      </select>
                    </label>

                    <label>
                      <span>Topic</span>
                      <select
                        value={mapping.topicId}
                        onChange={(event) => {
                          const value = event.target.value
                          handleTopicChange(file.id, mapping.id, value)
                          if (value) {
                            loadValidSubtopics(file.id, mapping.id, mapping.areaId, value)
                          }
                        }}
                        disabled={!mapping.areaId}
                      >
                        <option value="">Select topic</option>
                        {selectedAreaTopics(mapping.areaId).map((topic) => (
                          <option key={topic.id} value={topic.id}>
                            {topic.name}
                          </option>
                        ))}
                      </select>
                    </label>

                    <label>
                      <span>Status</span>
                      <select
                        value={mapping.status}
                        onChange={(event) =>
                          updateMapping(file.id, mapping.id, { status: event.target.value })
                        }
                        disabled={!mapping.areaId || !mapping.topicId}
                      >
                        <option value="Learning">Learning</option>
                        <option value="Done">Done</option>
                        <option value="Review">Review</option>
                      </select>
                    </label>
                  </div>

                  {mapping.areaId && mapping.topicId && (
                    <div className="subtopic-panel">
                      <h4>Valid subtopics</h4>
                      <div className="checkbox-grid">
                        {mapping.validSubtopics.length > 0 ? (
                          mapping.validSubtopics.map((subtopic) => (
                            <label key={subtopic} className="checkbox-item">
                              <input
                                type="checkbox"
                                checked={mapping.selectedSubtopics.includes(subtopic)}
                                onChange={() => toggleSubtopic(file.id, mapping.id, subtopic)}
                              />
                              <span>{subtopic}</span>
                            </label>
                          ))
                        ) : (
                          <p className="muted-text">Select a topic to load valid subtopics.</p>
                        )}
                      </div>
                    </div>
                  )}

                  <label className="notes-field">
                    <span>Your notes</span>
                    <textarea
                      value={mapping.noteText}
                      onChange={(event) =>
                        updateMapping(file.id, mapping.id, { noteText: event.target.value })
                      }
                      rows={5}
                      placeholder="Add detail about what you learned or what to revisit."
                      disabled={!mapping.areaId || !mapping.topicId}
                    />
                  </label>

                  <div className="mapping-actions">
                    <button
                      type="button"
                      className="secondary-button"
                      onClick={() => handlePreview(file.id, mapping.id)}
                      disabled={!mapping.areaId || !mapping.topicId || mapping.previewLoading}
                    >
                      {mapping.previewLoading ? 'Previewing...' : 'Preview'}
                    </button>
                  </div>

                  {mapping.previewError && (
                    <div className="error-box inline-error">
                      <p>{mapping.previewError}</p>
                    </div>
                  )}

                  {mapping.preview && (
                    <div className="preview-box">
                      <h4>Preview result</h4>

                      {mapping.preview.file_exists ? (
                        <>
                          <div className="mode-picker">
                            <label>
                              <input
                                type="radio"
                                name={`mode-${mapping.id}`}
                                value="append"
                                checked={mapping.mode === 'append'}
                                onChange={() => updateMapping(file.id, mapping.id, { mode: 'append' })}
                              />
                              Append
                            </label>
                            <label>
                              <input
                                type="radio"
                                name={`mode-${mapping.id}`}
                                value="overwrite"
                                checked={mapping.mode === 'overwrite'}
                                onChange={() => updateMapping(file.id, mapping.id, { mode: 'overwrite' })}
                              />
                              Overwrite
                            </label>
                          </div>

                          <div className="preview-columns">
                            <div>
                              <h5>Existing content</h5>
                              <pre>{mapping.preview.existing_content || '(empty file)'}</pre>
                            </div>
                            <div>
                              <h5>New section preview</h5>
                              <pre>{mapping.preview.new_section_preview}</pre>
                            </div>
                          </div>
                        </>
                      ) : (
                        <pre>{mapping.preview.new_section_preview}</pre>
                      )}
                    </div>
                  )}

                  {mapping.preview && (
                    <div className="approve-panel">
                      <button
                        type="button"
                        className="primary-button"
                        onClick={() => handleApprove(file.id, mapping.id)}
                        disabled={mapping.approveLoading || mapping.approved || (!mapping.preview ? true : false)}
                      >
                        {mapping.approveLoading ? 'Approving...' : 'Approve'}
                      </button>
                    </div>
                  )}

                  {mapping.approveError && (
                    <div className="error-box inline-error">
                      <p>{mapping.approveError}</p>
                      {mapping.approveResult?.saved_files?.length ? (
                        <div className="saved-files-list">
                          <strong>Saved locally:</strong>
                          <ul>
                            {mapping.approveResult.saved_files.map((path) => (
                              <li key={path}>{path}</li>
                            ))}
                          </ul>
                        </div>
                      ) : null}
                    </div>
                  )}

                  {mapping.approveResult && !mapping.approveError && (
                    <div className="card success-box approve-success-box">
                      <h4>Approved successfully</h4>
                      {mapping.approveResult.commit_sha && (
                        <p>Commit SHA: {mapping.approveResult.commit_sha}</p>
                      )}
                      <div className="saved-files-list">
                        <strong>Saved files:</strong>
                        <ul>
                          {mapping.approveResult.saved_files.map((path) => (
                            <li key={path}>{path}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              ))}

              <button
                type="button"
                className="secondary-button add-mapping-button"
                onClick={() => addAnotherMapping(file.id)}
              >
                + Add another mapping
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default UploadNotes
