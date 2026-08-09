import React, { useEffect, useRef, useState } from 'react'

/**
 * Animated circular score indicator (0 -> value, out of `max`).
 * Pure SVG + CSS, no library. Ring color shifts by band so the
 * candidate gets an at-a-glance read: green (strong), amber
 * (building), purple (early stage) - matching the tag colors already
 * used for the readiness score on the Dashboard.
 *
 * Props:
 *  - value: number (0-max)
 *  - max: number (default 100)
 *  - label: string shown under the number
 *  - duration: ms (default 1000)
 */
export default function ScoreRing({ value = 0, max = 100, label, duration = 1000 }) {
  const [display, setDisplay] = useState(0)
  const frameRef = useRef(null)

  useEffect(() => {
    const start = performance.now()
    function tick(now) {
      const elapsed = now - start
      const t = Math.min(1, elapsed / duration)
      const eased = 1 - Math.pow(1 - t, 3)
      setDisplay(Math.round(value * eased))
      if (t < 1) frameRef.current = requestAnimationFrame(tick)
    }
    frameRef.current = requestAnimationFrame(tick)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, duration])

  const pct = Math.max(0, Math.min(100, (value / max) * 100))
  const color = pct >= 70 ? 'var(--success)' : pct >= 40 ? 'var(--warning)' : 'var(--purple-400)'

  const size = 132
  const stroke = 10
  const r = (size - stroke) / 2
  const circumference = 2 * Math.PI * r
  const offset = circumference - (pct / 100) * circumference

  return (
    <div className="score-ring">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none"
          stroke="rgba(124,58,237,0.14)"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={{ transition: `stroke-dashoffset ${duration}ms cubic-bezier(0.16,1,0.3,1)` }}
        />
      </svg>
      <div className="score-ring-center">
        <span className="score-ring-value">{display}</span>
        <span className="score-ring-max">/ {max}</span>
      </div>
      {label && <span className="score-ring-label">{label}</span>}
    </div>
  )
}
