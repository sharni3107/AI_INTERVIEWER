import React, { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import ProgressBar from '../components/ProgressBar'
import SkillCoverage from '../components/SkillCoverage'
import { useCandidate } from '../context/CandidateContext'
import { getCurriculum } from '../services/api'
import { getCandidateStats } from '../utils/candidateStats'
import './Dashboard.css'

const MOTIVATION = 'Small progress every day builds extraordinary results.'

function greetingForNow() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}

function readinessTag(score) {
  if (score >= 70) return { label: 'Strong Foundation', tone: 'strong' }
  if (score >= 40) return { label: 'Building Momentum', tone: 'medium' }
  return { label: 'Early Stage', tone: 'low' }
}

export default function Dashboard() {
  const navigate = useNavigate()
  const { candidate } = useCandidate()
  const curriculum = getCurriculum()

  const stats = useMemo(
    () => (candidate ? getCandidateStats(candidate, curriculum) : null),
    [candidate, curriculum]
  )

  if (!candidate || !stats) return null

  const firstName = stats.candidate.name.split(' ')[0]
  const tag = readinessTag(stats.readinessScore)

  const topModules = [...stats.moduleBreakdown]
    .sort((a, b) => b.totalDays - a.totalDays)
    .slice(0, 3)
    .map((m) => ({ label: m.title, value: m.pct }))

  return (
    <div className="page-shell">
      <Navbar />
      <main className="dash-main">
        <div className="fade-slide-up">
          <h1 className="dash-greeting-title">
            {greetingForNow()}, {firstName}
          </h1>
          <p className="dash-greeting-sub">Keep learning. Keep building.</p>
        </div>

        <div className="dash-grid">
          <div className="glass-card dash-card dash-streak-card fade-slide-up" style={{ animationDelay: '80ms' }}>
            <span className="dash-card-label">Day Streak</span>
            <div className="dash-streak-row">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--warning)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M12 2c1.2 2.8-.4 4.2-1.6 5.6C9 9 8 10.4 8 12.4a4 4 0 108 0c0-1.3-.5-2-1-2.7 1.6.5 3 2.2 3 4.5a6 6 0 11-12 0c0-3.6 2.2-5.6 3.8-7.4C11 5.4 11.6 4 12 2z" />
              </svg>
              <div className="dash-stat-huge">{stats.candidate.commitDays}</div>
            </div>
            <div className="dash-stat-sub">days of active engagement this cohort</div>
          </div>

          <div className="glass-card dash-card fade-slide-up" style={{ animationDelay: '160ms' }}>
            <span className="dash-card-label">Course Progress</span>
            <div className="dash-stat-huge">
              {stats.daysCompletedCount} / {stats.totalDays}
            </div>
            <div className="dash-stat-sub" style={{ marginBottom: 12 }}>days completed</div>
            <ProgressBar value={stats.courseProgressPct} showPercent color="purple" />
          </div>

          <div className="glass-card dash-card fade-slide-up" style={{ animationDelay: '240ms' }}>
            <span className="dash-card-label">Interview Readiness</span>
            <div className="dash-readiness-score">
              {stats.readinessScore}
              <span> / 100</span>
            </div>
            <span className={`dash-readiness-tag ${tag.tone}`}>{tag.label}</span>
            <SkillCoverage items={topModules} />
          </div>
        </div>

        <div className="dash-row-2">
          <div className="glass-card dash-continue-card fade-slide-up" style={{ animationDelay: '320ms' }}>
            <div className="dash-continue-top">
              <div>
                <span className="dash-continue-day">
                  {stats.nextDay ? `Day ${stats.nextDay.day}` : 'Curriculum'}
                </span>
                <h3 className="dash-continue-title">
                  {stats.nextDay ? stats.nextDay.title : 'All days completed'}
                </h3>
              </div>
            </div>
            <ProgressBar
              value={stats.courseProgressPct}
              color="blue"
              showPercent={false}
              height={6}
            />
            <button
              className="btn-primary dash-continue-cta"
              onClick={() => navigate('/learning-journey')}
            >
              Continue →
            </button>
          </div>

          <div className="dash-side-stack">
            <div className="glass-card dash-card dash-note-card fade-slide-up" style={{ animationDelay: '380ms' }}>
              <div className="dash-note-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--purple-300)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="9" />
                  <circle cx="12" cy="12" r="4.5" />
                  <circle cx="12" cy="12" r="1" fill="var(--purple-300)" stroke="none" />
                </svg>
                <span className="dash-card-label">Today's Goal</span>
              </div>
              <p className="dash-goal-text">
                {stats.nextDay
                  ? `Review ${stats.nextDay.title}`
                  : 'Revisit any topic you want to strengthen further.'}
              </p>
            </div>
            <div className="glass-card dash-card dash-note-card fade-slide-up" style={{ animationDelay: '440ms' }}>
              <div className="dash-note-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--purple-300)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M12 3v3M12 18v3M4.2 6.3l2.1 2.1M17.7 15.6l2.1 2.1M3 12h3M18 12h3M4.2 17.7l2.1-2.1M17.7 8.4l2.1-2.1" />
                </svg>
                <span className="dash-card-label">Today's Motivation</span>
              </div>
              <p className="dash-quote-text">&ldquo;{MOTIVATION}&rdquo;</p>
            </div>
          </div>
        </div>

        <div className="dash-cta-bar fade-slide-up" style={{ animationDelay: '500ms' }}>
          <button className="btn-primary" onClick={() => navigate('/interview')}>
            Start AI Interview →
          </button>
        </div>
      </main>
    </div>
  )
}
