/**
 * Centralized API layer.
 *
 * Only ONE backend endpoint exists and is used here: POST /api/interview.
 * Its contract (verified against backend/app/schemas/interview.py and
 * backend/app/api/interviews.py):
 *
 *   Request:
 *     { sessionId: string, candidate?: object, message?: string }
 *
 *   Response:
 *     { reply: string, done: boolean, feedback?: { summary, strengths[], gaps[], next[] } }
 *
 * Candidate and curriculum data are NOT served by any backend endpoint,
 * so they are bundled as static JSON in src/data/ (mirrors
 * backend/data/candidates.json and backend/data/curriculum.json) and
 * read locally by getCandidateById / getAllCandidates / getCurriculum.
 */

import candidatesData from '../data/candidates.json'
import curriculumData from '../data/curriculum.json'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8010'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function postInterview(body) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/api/interview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch (networkError) {
    throw new ApiError(
      'Unable to connect to the interview service.',
      0
    )
  }

  let data = null
  try {
    data = await response.json()
  } catch {
    // ignore parse failure, handled below via !response.ok
  }

  if (!response.ok) {
    const detail = data?.detail || data?.error || 'Something went wrong. Please try again.'
    throw new ApiError(detail, response.status)
  }

  return data
}

/**
 * Starts a new interview session for the given candidate.
 * The backend generates the opening question; the frontend
 * generates and owns the sessionId.
 */
export function startInterview(sessionId, candidateRaw) {
  return postInterview({ sessionId, candidate: candidateRaw })
}

/**
 * Submits the candidate's answer and reuses the existing sessionId.
 * Returns the next question, or the final result when `done` is true.
 */
export function sendInterviewMessage(sessionId, message) {
  return postInterview({ sessionId, message })
}

/**
 * Candidate lookup. No backend endpoint exists for this, so it reads
 * the bundled copy of backend/data/candidates.json.
 */
export function getCandidateById(candidateId) {
  const normalized = String(candidateId || '').trim().toUpperCase()

  const found = (candidatesData.candidates || []).find(
    (c) => String(c.member?.id || '').toUpperCase() === normalized
  )

  return found || null
}

export function getAllCandidates() {
  return candidatesData.candidates || []
}

/**
 * Curriculum lookup. No backend endpoint exists for this, so it reads
 * the bundled copy of backend/data/curriculum.json.
 */
export function getCurriculum() {
  return curriculumData
}
