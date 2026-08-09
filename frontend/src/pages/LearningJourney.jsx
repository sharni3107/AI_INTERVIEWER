import React, { useMemo, useRef, useState } from 'react'
import Navbar from '../components/Navbar'
import ProgressBar from '../components/ProgressBar'
import LearningTimeline from '../components/LearningTimeline'
import { useCandidate } from '../context/CandidateContext'
import { getCurriculum } from '../services/api'
import { getCandidateStats } from '../utils/candidateStats'
import useScrollProgress from '../hooks/useScrollProgress'
import './LearningJourney.css'

function dayStatus(day, stats) {
  if (stats.candidate.passedDays.includes(day)) return { key: 'completed', label: 'Completed' }
  if (stats.candidate.failedDays.includes(day)) return { key: 'failed', label: 'Needs Review' }
  if (stats.candidate.skippedDays.includes(day)) return { key: 'skipped', label: 'Skipped' }
  if (stats.nextDay && stats.nextDay.day === day) return { key: 'progress', label: 'In Progress' }
  return { key: 'locked', label: 'Locked' }
}

export default function LearningJourney() {
  const { candidate } = useCandidate()
  const curriculum = getCurriculum()
  const [showFullCurriculum, setShowFullCurriculum] = useState(false)
  const phasesRef = useRef(null)
  const scrollProgress = useScrollProgress(phasesRef)

  const stats = useMemo(
    () => (candidate ? getCandidateStats(candidate, curriculum) : null),
    [candidate, curriculum]
  )

  if (!candidate || !stats) return null

  const phases = stats.moduleBreakdown.map((m) => ({
    n: m.n,
    title: m.title,
    description: `Days ${m.startDay}\u2013${m.endDay}`,
    progress: m.pct,
    startDay: m.startDay,
    endDay: m.endDay,
  }))

  const activePhaseIndex = stats.nextDay
    ? phases.findIndex((p) => stats.nextDay.day >= p.startDay && stats.nextDay.day <= p.endDay)
    : -1

  const days = [...(curriculum.days || [])].sort((a, b) => a.day - b.day)

  return (
    <div className="page-shell">
      <Navbar
        title="Learning Journey"
        showBack
        backTo="/dashboard"
        right={
          <button
            className="lj-filter-btn"
            aria-label="Toggle full curriculum list"
            onClick={() => setShowFullCurriculum((v) => !v)}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <line x1="4" y1="6" x2="20" y2="6" />
              <line x1="7" y1="12" x2="17" y2="12" />
              <line x1="10" y1="18" x2="14" y2="18" />
            </svg>
          </button>
        }
      />
      <main className="lj-main">
        <div className="glass-card lj-overall-card fade-slide-up">
          <div className="lj-overall-top">
            <div>
              <span className="lj-overall-label">Overall Progress</span>
              <h2 className="lj-overall-title">{curriculum.cohort || '31-Day AI Engineering Cohort'}</h2>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div className="lj-overall-pct">{stats.courseProgressPct}%</div>
              <div className="lj-overall-days">
                {stats.daysCompletedCount} / {stats.totalDays} days completed
              </div>
            </div>
          </div>
          <ProgressBar value={stats.courseProgressPct} showPercent={false} duration={1100} />
        </div>

        <section ref={phasesRef}>
          <h3 className="lj-section-title">Course Roadmap ({phases.length} Phases)</h3>
          <LearningTimeline
            phases={phases}
            activePhaseIndex={activePhaseIndex}
            scrollProgress={scrollProgress}
          />

          <button
            className="btn-secondary lj-view-all"
            onClick={() => setShowFullCurriculum((v) => !v)}
          >
            {showFullCurriculum ? 'Hide full curriculum' : `View full ${stats.totalDays}-day curriculum →`}
          </button>

          {showFullCurriculum && (
            <div className="lj-curriculum-list fade-in">
              {days.map((d) => {
                const status = dayStatus(d.day, stats)
                return (
                  <div key={d.day} className={`lj-day-row${status.key === 'locked' ? ' locked' : ''}`}>
                    <div className="lj-day-left">
                      <span className="lj-day-num">Day {d.day}</span>
                      <span className="lj-day-title">{d.title}</span>
                    </div>
                    <span className={`lj-day-status ${status.key}`}>{status.label}</span>
                  </div>
                )
              })}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
