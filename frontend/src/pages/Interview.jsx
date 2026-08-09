import React, { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import ProgressBar from '../components/ProgressBar'
import QuestionCard from '../components/QuestionCard'
import { useCandidate } from '../context/CandidateContext'
import { startInterview, sendInterviewMessage, ApiError } from '../services/api'
import './Interview.css'

// The backend enforces a real minimum (INTERVIEW_MIN_QUESTIONS=8) and max
// (INTERVIEW_MAX_QUESTIONS=16), but never reports counts back to the
// client. This is only a display estimate for the progress bar - the
// actual end of the interview is always driven by the backend's `done`
// flag, never by this number.
const ESTIMATED_TOTAL_QUESTIONS = 8

const RULES = [
  {
    title: 'Full screen required',
    desc: 'Stay in full-screen mode for the whole session so nothing else competes for your attention.',
    icon: (
      <path d="M4 9V5a1 1 0 011-1h4M20 9V5a1 1 0 00-1-1h-4M4 15v4a1 1 0 001 1h4M20 15v4a1 1 0 01-1 1h-4" />
    ),
  },
  {
    title: 'Stay on this page',
    desc: 'Switching tabs or apps may pause or flag your session - keep this the only thing open.',
    icon: (
      <>
        <rect x="3.5" y="4.5" width="17" height="13" rx="2" />
        <path d="M8 20h8M12 17.5V20" />
      </>
    ),
  },
  {
    title: 'Text responses only',
    desc: 'Answer in the composer below - no audio or video responses are evaluated.',
    icon: (
      <>
        <path d="M4 5h16M4 10h16M4 15h10" />
      </>
    ),
  },
  {
    title: 'Adaptive questions',
    desc: 'Each question is generated from your previous answer and curriculum progress - there is no fixed question bank.',
    icon: (
      <>
        <path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7L12 3z" />
      </>
    ),
  },
]

const SESSION_KEY = 'interview_session_id'
const QUESTION_NUMBER_KEY = 'interview_question_number'
const CURRENT_QUESTION_KEY = 'interview_current_question'

export default function Interview() {
  const navigate = useNavigate()
  const { candidate } = useCandidate()

  const [sessionId, setSessionId] = useState(null)
  const [questionNumber, setQuestionNumber] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [starting, setStarting] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const initRef = useRef(false)

  useEffect(() => {
    if (initRef.current) return
    initRef.current = true
    initSession()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function initSession() {
    setStarting(true)
    setError(null)

    const storedSession = sessionStorage.getItem(SESSION_KEY)
    const storedQuestion = sessionStorage.getItem(CURRENT_QUESTION_KEY)
    const storedNumber = sessionStorage.getItem(QUESTION_NUMBER_KEY)

    if (storedSession && storedQuestion) {
      // Resume in place - re-uses the sessionId, doesn't call the
      // backend again until the candidate submits an answer.
      setSessionId(storedSession)
      setCurrentQuestion(storedQuestion)
      setQuestionNumber(Number(storedNumber) || 1)
      setStarting(false)
      return
    }

    const newSessionId = crypto.randomUUID()

    try {
      const result = await startInterview(newSessionId, candidate)
      setSessionId(newSessionId)
      setCurrentQuestion(result.reply)
      setQuestionNumber(1)

      sessionStorage.setItem(SESSION_KEY, newSessionId)
      sessionStorage.setItem(CURRENT_QUESTION_KEY, result.reply)
      sessionStorage.setItem(QUESTION_NUMBER_KEY, '1')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Unable to connect to the interview service.')
    } finally {
      setStarting(false)
    }
  }

  async function handleAnswer(answer) {
    if (!sessionId || submitting) return
    setSubmitting(true)
    setError(null)

    try {
      const result = await sendInterviewMessage(sessionId, answer)

      if (result.done) {
        sessionStorage.removeItem(SESSION_KEY)
        sessionStorage.removeItem(CURRENT_QUESTION_KEY)
        sessionStorage.removeItem(QUESTION_NUMBER_KEY)

        sessionStorage.setItem(
          'interview_result',
          JSON.stringify({
            feedback: result.feedback,
            questionsAsked: questionNumber,
            reply: result.reply,
          })
        )

        navigate('/results')
        return
      }

      const nextNumber = questionNumber + 1
      setCurrentQuestion(result.reply)
      setQuestionNumber(nextNumber)

      sessionStorage.setItem(CURRENT_QUESTION_KEY, result.reply)
      sessionStorage.setItem(QUESTION_NUMBER_KEY, String(nextNumber))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Unable to connect to the interview service.')
    } finally {
      setSubmitting(false)
    }
  }

  function handleEnd() {
    const confirmed = window.confirm('End this interview now? Your progress on this session will be lost.')
    if (!confirmed) return

    sessionStorage.removeItem(SESSION_KEY)
    sessionStorage.removeItem(CURRENT_QUESTION_KEY)
    sessionStorage.removeItem(QUESTION_NUMBER_KEY)
    navigate('/dashboard')
  }

  if (!candidate) return null

  const progressPct = Math.min(100, Math.round((questionNumber / ESTIMATED_TOTAL_QUESTIONS) * 100))

  return (
    <div className="page-shell">
      <Navbar
        title="AI Interview"
        showBack
        backTo="/dashboard"
        right={
          <button className="btn-secondary" onClick={handleEnd}>
            End
          </button>
        }
      />
      <main className="iv-main">
        {!starting && !error && (
          <div className="fade-slide-up">
            <div className="iv-progress-row">
              <span>Question {questionNumber} of {ESTIMATED_TOTAL_QUESTIONS}</span>
              <span>{progressPct}%</span>
            </div>
            <ProgressBar value={progressPct} showPercent={false} duration={600} />
          </div>
        )}

        {starting && (
          <div className="glass-card iv-loading-card fade-in">
            <span className="spinner" />
            <span className="iv-loading-text">Starting interview...</span>
          </div>
        )}

        {error && (
          <div className="glass-card iv-error-card fade-in">
            <p className="iv-error-title">Something went wrong</p>
            <p className="iv-error-text">{error}</p>
            <button className="btn-primary" onClick={initSession}>
              Retry
            </button>
          </div>
        )}

        {!starting && !error && currentQuestion && (
          <QuestionCard
            questionNumber={questionNumber}
            question={currentQuestion}
            loading={submitting}
            onSubmit={handleAnswer}
          />
        )}

        {!starting && (
          <div className="glass-card iv-rules-card fade-slide-up" style={{ animationDelay: '120ms' }}>
            <p className="iv-rules-title">Interview Rules</p>
            <ul className="iv-rules-list">
              {RULES.map((rule) => (
                <li key={rule.title}>
                  <span className="iv-rule-icon" aria-hidden="true">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      {rule.icon}
                    </svg>
                  </span>
                  <span className="iv-rule-copy">
                    <span className="iv-rule-title">{rule.title}</span>
                    <span className="iv-rule-desc">{rule.desc}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  )
}
