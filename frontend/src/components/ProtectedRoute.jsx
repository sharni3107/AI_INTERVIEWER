import React from 'react'
import { Navigate } from 'react-router-dom'
import { useCandidate } from '../context/CandidateContext'

export default function ProtectedRoute({ children }) {
  const { candidate, ready } = useCandidate()

  if (!ready) return null
  if (!candidate) return <Navigate to="/login" replace />

  return children
}
