import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCandidate } from '../context/CandidateContext'
import { getAllCandidates } from '../services/api'
import EntryIllustration from '../components/EntryIllustration'
import './Login.css'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useCandidate()

  const [candidateId, setCandidateId] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showDemo, setShowDemo] = useState(false)

  const allCandidates = getAllCandidates()

  function attemptLogin(id) {
    setError('')
    setLoading(true)

    // Candidate identification only - not password auth. Simulated
    // latency keeps the loading state meaningful for the demo.
    setTimeout(() => {
      const found = login(id)
      setLoading(false)

      if (!found) {
        setError('Candidate not found. Please check your Candidate ID and try again.')
        return
      }

      navigate('/dashboard')
    }, 400)
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!candidateId.trim() || loading) return
    attemptLogin(candidateId.trim())
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-brand">
          <span className="login-brand-mark" aria-hidden="true" />
          <span className="login-brand-text">
            <span className="login-brand-abtalks">ABTalks</span>
            <span className="login-brand-sub">AI Interviewer</span>
          </span>
        </div>

        <div className="login-illustration-wrap">
          <EntryIllustration />
        </div>

        <h1 className="login-heading">Welcome back</h1>
        <p className="login-subheading">Continue your AI engineering journey.</p>

        <form onSubmit={handleSubmit}>
          <label className="login-field-label" htmlFor="candidate-id">
            Enter your ID
          </label>
          <input
            id="candidate-id"
            className={`login-input${error ? ' error' : ''}`}
            placeholder="Ex. CAND-001"
            value={candidateId}
            onChange={(e) => {
              setCandidateId(e.target.value)
              if (error) setError('')
            }}
            autoComplete="off"
            aria-invalid={!!error}
            aria-describedby={error ? 'candidate-id-error' : undefined}
          />
          {error && (
            <p className="login-error" id="candidate-id-error">
              {error}
            </p>
          )}

          <button type="submit" className="btn-primary login-submit" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner" /> Verifying candidate...
              </>
            ) : (
              'Continue →'
            )}
          </button>
        </form>

        <button
          type="button"
          className="login-demo-toggle"
          onClick={() => setShowDemo((v) => !v)}
        >
          {showDemo ? 'Hide demo candidates' : 'Demo candidate'}
        </button>

        {showDemo && (
          <div className="login-demo-list">
            {allCandidates.map((c) => (
              <button
                key={c.member.id}
                type="button"
                className="login-demo-item"
                onClick={() => attemptLogin(c.member.id)}
              >
                <div>
                  <div className="login-demo-item-name">{c.member.name}</div>
                  <div className="login-demo-item-role">{c.member.jobRole}</div>
                </div>
                <span className="login-demo-item-id">{c.member.id}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
