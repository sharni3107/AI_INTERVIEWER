import React, { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import ScoreRing from '../components/ScoreRing'
import SkillCoverage from '../components/SkillCoverage'
import { useCandidate } from '../context/CandidateContext'
import { getCurriculum } from '../services/api'
import { getCandidateStats } from '../utils/candidateStats'
import './Results.css'

const RESULT_KEY = 'interview_result'

function readinessTag(score) {
  if (score >= 70) return { label: 'Strong Foundation', tone: 'strong' }
  if (score >= 40) return { label: 'Building Momentum', tone: 'medium' }
  return { label: 'Early Stage', tone: 'low' }
}

export default function Results() {
  const navigate = useNavigate()
  const { candidate } = useCandidate()
  const [result, setResult] = useState(undefined)
  const curriculum = getCurriculum()

  const stats = useMemo(
    () => (candidate ? getCandidateStats(candidate, curriculum) : null),
    [candidate, curriculum]
  )

  useEffect(() => {
    const raw = sessionStorage.getItem(RESULT_KEY)
    if (!raw) {
      setResult(null)
      return
    }
    try {
      setResult(JSON.parse(raw))
    } catch {
      setResult(null)
    }
  }, [])

  // No completed interview to show - don't allow arbitrary access to Results.
  useEffect(() => {
    if (result === null) navigate('/dashboard', { replace: true })
  }, [result, navigate])

  if (!candidate || !result) return null

  const { feedback, questionsAsked } = result
  const tag = stats ? readinessTag(stats.readinessScore) : null
  const knowledgeModules = stats
    ? stats.moduleBreakdown.map((m) => ({ label: m.title, value: m.pct }))
    : []

  function handleDownload() {
    const lines = [
      `AI Interview Report`,
      `Candidate: ${candidate.member?.name} (${candidate.member?.id})`,
      `Role: ${candidate.member?.jobRole}`,
      `Questions evaluated: ${questionsAsked}`,
      '',
      'Summary',
      '-------',
      feedback?.summary || '',
      '',
      'Strengths',
      '---------',
      ...(feedback?.strengths || []).map((s) => `- ${s}`),
      '',
      'Gaps',
      '----',
      ...(feedback?.gaps || []).map((g) => `- ${g}`),
      '',
      'Next Steps',
      '----------',
      ...(feedback?.next || []).map((n) => `- ${n}`),
    ]

    const blob = new Blob([lines.join('\n')], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `interview-report-${candidate.member?.id || 'candidate'}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="page-shell">
      <Navbar title="Results" showBack backTo="/dashboard" />
      <main className="res-main">
        <div className="glass-card res-hero fade-slide-up">
          <div className="res-badge">✓</div>
          <h1 className="res-title">Interview Complete</h1>
          <p className="res-subtitle">{questionsAsked} questions evaluated</p>
        </div>

        {stats && (
          <div className="glass-card res-score-card fade-slide-up" style={{ animationDelay: '40ms' }}>
            <ScoreRing value={stats.readinessScore} label="Readiness Score" />
            <div className="res-score-side">
              <span className={`res-readiness-tag ${tag.tone}`}>{tag.label}</span>
              <p className="res-score-note">
                Based on your learning-journey pass rate and first-try accuracy across the
                cohort curriculum - not a score from this interview conversation itself,
                since the AI interviewer doesn't return a numeric grade.
              </p>
            </div>
          </div>
        )}

        {knowledgeModules.length > 0 && (
          <div className="glass-card res-section fade-slide-up" style={{ animationDelay: '60ms' }}>
            <h3 className="res-section-title">Knowledge Level by Module</h3>
            <SkillCoverage items={knowledgeModules} />
          </div>
        )}

        {feedback?.summary && (
          <div className="glass-card res-section fade-slide-up" style={{ animationDelay: '80ms' }}>
            <h3 className="res-section-title">Summary</h3>
            <p className="res-summary-text">{feedback.summary}</p>
          </div>
        )}

        {feedback?.strengths?.length > 0 && (
          <div className="glass-card res-section fade-slide-up" style={{ animationDelay: '160ms' }}>
            <h3 className="res-section-title strengths">Strengths</h3>
            <ul className="res-list" style={{ color: 'var(--success)' }}>
              {feedback.strengths.map((s, i) => (
                <li key={i} style={{ color: 'var(--text-secondary)' }}>{s}</li>
              ))}
            </ul>
          </div>
        )}

        {feedback?.gaps?.length > 0 && (
          <div className="glass-card res-section fade-slide-up" style={{ animationDelay: '240ms' }}>
            <h3 className="res-section-title gaps">Gaps</h3>
            <ul className="res-list" style={{ color: 'var(--warning)' }}>
              {feedback.gaps.map((g, i) => (
                <li key={i} style={{ color: 'var(--text-secondary)' }}>{g}</li>
              ))}
            </ul>
          </div>
        )}

        {feedback?.next?.length > 0 && (
          <div className="glass-card res-section fade-slide-up" style={{ animationDelay: '320ms' }}>
            <h3 className="res-section-title next">Next Steps</h3>
            <ul className="res-list" style={{ color: 'var(--purple-300)' }}>
              {feedback.next.map((n, i) => (
                <li key={i} style={{ color: 'var(--text-secondary)' }}>{n}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="res-actions fade-slide-up" style={{ animationDelay: '400ms' }}>
          <button className="btn-primary" onClick={handleDownload}>
            Download Full Report
          </button>
          <button className="btn-secondary" onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </button>
        </div>
      </main>
    </div>
  )
}