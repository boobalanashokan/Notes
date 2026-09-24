import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { getTracks } from './api'

const TrackContext = createContext(null)

export function TrackProvider({ children }) {
  const [tracks, setTracks] = useState([])
  const [trackId, setTrackIdState] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadTracks() {
      try {
        const data = await getTracks()
        if (ignore) {
          return
        }

        const nextTracks = Array.isArray(data) ? data : []
        setTracks(nextTracks)

        const savedTrackId = localStorage.getItem('selectedTrackId')
        const fallbackTrackId = nextTracks[0]?.id || ''
        const resolvedTrackId = nextTracks.some((track) => track.id === savedTrackId)
          ? savedTrackId
          : fallbackTrackId

        setTrackIdState(resolvedTrackId)

        if (resolvedTrackId) {
          localStorage.setItem('selectedTrackId', resolvedTrackId)
        } else {
          localStorage.removeItem('selectedTrackId')
        }

        setError('')
      } catch (err) {
        if (!ignore) {
          setTracks([])
          setTrackIdState('')
          setError(err.message || 'Could not load tracks.')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadTracks()
    return () => {
      ignore = true
    }
  }, [])

  useEffect(() => {
    if (!tracks.length) {
      if (!trackId) {
        setTrackIdState('')
      }
      return
    }

    const exists = tracks.some((track) => track.id === trackId)
    if (!exists) {
      const fallbackTrackId = tracks[0].id
      setTrackIdState(fallbackTrackId)
      localStorage.setItem('selectedTrackId', fallbackTrackId)
    }
  }, [tracks, trackId])

  const setTrackId = (nextTrackId) => {
    setTrackIdState(nextTrackId || '')
    if (nextTrackId) {
      localStorage.setItem('selectedTrackId', nextTrackId)
    } else {
      localStorage.removeItem('selectedTrackId')
    }
  }

  const value = useMemo(() => ({
    tracks,
    trackId,
    setTrackId,
    trackName: tracks.find((track) => track.id === trackId)?.name || '',
    loading,
    error,
  }), [tracks, trackId, loading, error])

  return <TrackContext.Provider value={value}>{children}</TrackContext.Provider>
}

export function useTrack() {
  const context = useContext(TrackContext)
  if (!context) {
    throw new Error('useTrack must be used within a TrackProvider')
  }
  return context
}
