import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import './App.css'
import Dashboard from './pages/Dashboard'
import Roadmap from './pages/Roadmap'
import UploadNotes from './pages/UploadNotes'

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <nav className="topnav">
          <div className="brand">Study Tracker</div>
          <div className="nav-links">
            <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              Dashboard
            </NavLink>
            <NavLink to="/roadmap" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              Roadmap
            </NavLink>
            <NavLink to="/upload" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
              Upload Notes
            </NavLink>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/roadmap" element={<Roadmap />} />
            <Route path="/upload" element={<UploadNotes />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
