import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import './App.css'
import { TrackProvider, useTrack } from './TrackContext'
import AddTrack from './pages/AddTrack'
import Dashboard from './pages/Dashboard'
import Notes from './pages/Notes'
import Projects from './pages/Projects'
import Roadmap from './pages/Roadmap'
import Skills from './pages/Skills'
import UploadNotes from './pages/UploadNotes'

function AppShell() {
  const { tracks, trackId, setTrackId, loading } = useTrack()

  return (
    <div className="app-shell">
      <nav className="topnav">
        <div className="brand" aria-label="StudyTracker brand">
          <span className="brand-mark">✦</span>
          <span className="brand-text">Study<span>Tracker</span></span>
        </div>

        <div className="nav-controls">
          <label className="track-switcher" aria-label="Select track">
            <span className="track-switcher-label">Track</span>
            <select
              value={trackId}
              onChange={(event) => setTrackId(event.target.value)}
              disabled={loading || tracks.length === 0}
            >
              {tracks.length === 0 ? <option value="">Loading tracks...</option> : null}
              {tracks.map((track) => (
                <option key={track.id} value={track.id}>
                  {track.name}
                </option>
              ))}
            </select>
          </label>

          <div className="nav-links">
            <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">⌂</span>
              <span>Dashboard</span>
            </NavLink>
            <NavLink to="/notes" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">☰</span>
              <span>Notes</span>
            </NavLink>
            <NavLink to="/roadmap" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">◫</span>
              <span>Roadmap</span>
            </NavLink>
            <NavLink to="/projects" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">▣</span>
              <span>Projects</span>
            </NavLink>
            <NavLink to="/skills" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">✧</span>
              <span>Skills</span>
            </NavLink>
            <NavLink to="/add-track" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">＋</span>
              <span>Add Track</span>
            </NavLink>
            <NavLink to="/upload" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              <span className="nav-icon">⇪</span>
              <span>Upload Notes</span>
            </NavLink>
          </div>
        </div>

        <div className="profile-toggle" aria-label="User profile">
          <span className="profile-dot" />
        </div>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/notes" element={<Notes />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/skills" element={<Skills />} />
          <Route path="/add-track" element={<AddTrack />} />
          <Route path="/upload" element={<UploadNotes />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <TrackProvider>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </TrackProvider>
  )
}

export default App
