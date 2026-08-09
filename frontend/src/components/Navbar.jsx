import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useCandidate } from '../context/CandidateContext'
import '../styles/components.css'

/**
 * Top navigation/header.
 *
 * Props:
 *  - title: string shown as the page title (e.g. "Learning Journey")
 *  - showBack: boolean, renders a back button
 *  - backTo: path for back navigation (default: browser back)
 *  - right: optional extra node rendered before the candidate/logout controls
 */
export default function Navbar({ title, showBack = false, backTo, right }) {
  const navigate = useNavigate()
  const { candidate, logout } = useCandidate()

  function handleBack() {
    if (backTo) navigate(backTo)
    else navigate(-1)
  }

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const initials = candidate?.member?.name
    ?.split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase() || '?'

  return (
    <header className="navbar">
      <div className="navbar-brand">
        {showBack ? (
          <button className="navbar-back" onClick={handleBack} aria-label="Go back">
            ← {title || 'Back'}
          </button>
        ) : (
          <>
            <span className="navbar-brand-mark" aria-hidden="true" />
            <span className="navbar-brand-text">
              <span className="navbar-brand-abtalks">ABTalks</span>
              <span className="navbar-brand-sub">AI Interviewer</span>
            </span>
          </>
        )}
      </div>

      <div className="navbar-actions">
        {right}
        {candidate && (
          <div className="navbar-candidate">
            <span className="navbar-avatar">{initials}</span>
            <span className="navbar-candidate-name">{candidate.member?.name}</span>
          </div>
        )}
        {candidate && (
          <button className="navbar-logout" onClick={handleLogout} aria-label="Log out">
            Logout
          </button>
        )}
      </div>
    </header>
  )
}
