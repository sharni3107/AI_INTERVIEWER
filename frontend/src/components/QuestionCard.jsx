import React, { useState } from 'react'
import '../styles/components.css'

const MAX_CHARS = 1000

/**
 * Renders a single interview question with an answer textarea.
 *
 * Props:
 *  - questionNumber: number
 *  - question: string
 *  - loading: boolean (submitting/evaluating)
 *  - onSubmit: (answer: string) => void
 */
export default function QuestionCard({ questionNumber, question, loading, onSubmit }) {
  const [answer, setAnswer] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = answer.trim()
    if (!trimmed || loading) return
    onSubmit(trimmed)
    setAnswer('')
  }

  return (
    <form className="question-card glass-card" onSubmit={handleSubmit}>
      <div className="question-eyebrow">
        <span className="question-eyebrow-dot" />
        AI Interviewer
      </div>

      <p className="question-text">{question}</p>

      <label className="question-answer-label" htmlFor="interview-answer">
        Your answer
      </label>
      <textarea
        id="interview-answer"
        className="question-textarea"
        placeholder="Type your answer here..."
        value={answer}
        maxLength={MAX_CHARS}
        onChange={(e) => setAnswer(e.target.value)}
        disabled={loading}
        aria-label={`Answer to question ${questionNumber}`}
      />

      <div className="question-footer">
        <span className="question-char-count">
          {answer.length} / {MAX_CHARS}
        </span>
        <button type="submit" className="btn-primary" disabled={loading || !answer.trim()}>
          {loading ? (
            <>
              <span className="spinner" /> Evaluating...
            </>
          ) : (
            'Submit Answer'
          )}
        </button>
      </div>
    </form>
  )
}
