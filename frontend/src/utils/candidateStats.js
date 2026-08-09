/**
 * Derives display-ready stats from a raw candidate record
 * ({ member, missions, signals }) and the curriculum.
 *
 * This mirrors the shape backend/app/utils/candidate_normalizer.py
 * derives server-side (passed/failed/skipped/struggled days), but is
 * computed client-side purely for UI display since no backend endpoint
 * exposes computed candidate progress.
 */

export function normalizeCandidate(candidate) {
  const member = candidate?.member || {}
  const missions = candidate?.missions || []
  const signals = candidate?.signals || {}

  const completed = missions.filter((m) => m && m.day != null && !m.skipped)
  const skipped = missions.filter((m) => m && m.day != null && m.skipped)

  const passedDays = [...new Set(completed.filter((m) => m.passed === true).map((m) => m.day))].sort((a, b) => a - b)
  const failedDays = [...new Set(completed.filter((m) => m.passed === false).map((m) => m.day))].sort((a, b) => a - b)
  const skippedDays = [...new Set(skipped.map((m) => m.day))].sort((a, b) => a - b)
  const attemptedDays = [...new Set(completed.map((m) => m.day))].sort((a, b) => a - b)

  const highAttempt = completed.filter((m) => typeof m.attempts === 'number' && m.attempts >= 3).map((m) => m.day)
  const struggledDays = [...new Set([...highAttempt, ...failedDays])].sort((a, b) => a - b)

  return {
    id: member.id || 'UNKNOWN',
    name: member.name || 'Candidate',
    jobRole: member.jobRole || '',
    yearsExperience: member.yearsExperience,
    education: member.education || '',
    status: member.status || '',
    missions,
    passedDays,
    failedDays,
    skippedDays,
    attemptedDays,
    struggledDays,
    commitDays: signals.commitDays ?? 0,
    missionsCompleted: signals.missionsCompleted ?? 0,
    missionsFirstTry: signals.missionsFirstTry ?? 0,
  }
}

export function getCandidateStats(candidate, curriculum) {
  const n = normalizeCandidate(candidate)
  const days = curriculum?.days || []
  const modules = curriculum?.modules || []
  const totalDays = days.length || 31

  const daysCompletedCount = n.passedDays.length
  const courseProgressPct = totalDays > 0
    ? Math.round((daysCompletedCount / totalDays) * 100)
    : 0

  const firstTryRate = n.missionsCompleted > 0
    ? n.missionsFirstTry / n.missionsCompleted
    : 0

  const passRate = totalDays > 0 ? daysCompletedCount / totalDays : 0

  const readinessScore = Math.max(
    0,
    Math.min(100, Math.round((passRate * 0.6 + firstTryRate * 0.4) * 100))
  )

  const moduleBreakdown = modules.map((mod) => {
    const [start, end] = mod.days || [0, 0]
    const moduleDays = days.filter((d) => d.day >= start && d.day <= end)
    const moduleDayNumbers = moduleDays.map((d) => d.day)
    const passedInModule = moduleDayNumbers.filter((d) => n.passedDays.includes(d))
    const pct = moduleDayNumbers.length > 0
      ? Math.round((passedInModule.length / moduleDayNumbers.length) * 100)
      : 0

    return {
      n: mod.n,
      title: mod.title,
      startDay: start,
      endDay: end,
      totalDays: moduleDayNumbers.length,
      passedCount: passedInModule.length,
      pct,
    }
  })

  const dayTitleMap = {}
  days.forEach((d) => { dayTitleMap[d.day] = d.title })

  const nextDayNumber = days
    .map((d) => d.day)
    .sort((a, b) => a - b)
    .find((d) => !n.passedDays.includes(d) && !n.skippedDays.includes(d))

  const nextDay = nextDayNumber
    ? { day: nextDayNumber, title: dayTitleMap[nextDayNumber] || `Day ${nextDayNumber}` }
    : null

  return {
    candidate: n,
    totalDays,
    daysCompletedCount,
    courseProgressPct,
    readinessScore,
    moduleBreakdown,
    nextDay,
    dayTitleMap,
  }
}
