import React, { createContext, useContext, useEffect, useState } from 'react'
import { getCandidateById } from '../services/api'

const CandidateContext = createContext(null)

const STORAGE_KEY = 'candidate_id'

export function CandidateProvider({ children }) {
  const [candidate, setCandidate] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const storedId = sessionStorage.getItem(STORAGE_KEY)
    if (storedId) {
      const found = getCandidateById(storedId)
      if (found) setCandidate(found)
    }
    setReady(true)
  }, [])

  function login(candidateId) {
    const found = getCandidateById(candidateId)
    if (!found) return null

    sessionStorage.setItem(STORAGE_KEY, found.member.id)
    setCandidate(found)
    return found
  }

  function logout() {
    sessionStorage.removeItem(STORAGE_KEY)
    sessionStorage.removeItem('interview_session_id')
    sessionStorage.removeItem('interview_question_number')
    sessionStorage.removeItem('interview_result')
    setCandidate(null)
  }

  return (
    <CandidateContext.Provider value={{ candidate, login, logout, ready }}>
      {children}
    </CandidateContext.Provider>
  )
}

export function useCandidate() {
  const ctx = useContext(CandidateContext)
  if (!ctx) throw new Error('useCandidate must be used within CandidateProvider')
  return ctx
}
