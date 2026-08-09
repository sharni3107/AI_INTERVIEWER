import React from 'react'

/**
 * Minimal abstract AI/circuit mark shown on the Login screen - a
 * dotted orbit ring, spoke lines to small circuit nodes, and a
 * glowing core. Deliberately not a user/avatar icon - purely
 * abstract neural-network geometry. Pure inline SVG, no external
 * assets.
 */
export default function EntryIllustration() {
  const nodes = [
    [100, 30],
    [155, 58],
    [155, 142],
    [100, 170],
    [45, 142],
    [45, 58],
  ]

  return (
    <svg viewBox="0 0 200 200" width="132" height="132" className="entry-illustration">
      <defs>
        <radialGradient id="coreGrad" cx="40%" cy="35%" r="75%">
          <stop offset="0%" stopColor="#C084FC" />
          <stop offset="100%" stopColor="#5B21B6" />
        </radialGradient>
      </defs>

      <circle
        cx="100" cy="100" r="78"
        fill="none"
        stroke="rgba(124,58,237,0.18)"
        strokeWidth="1.5"
        strokeDasharray="2 7"
      />

      {nodes.map(([x, y], i) => (
        <line
          key={`l-${i}`}
          x1="100" y1="100" x2={x} y2={y}
          stroke="rgba(139,92,246,0.32)"
          strokeWidth="1"
        />
      ))}

      {nodes.map(([x, y], i) => (
        <circle key={`n-${i}`} cx={x} cy={y} r="4" fill="#08080F" stroke="#8B5CF6" strokeWidth="1.5" />
      ))}

      {/* small circuit accent ticks */}
      {nodes.map(([x, y], i) => {
        const dx = x - 100
        const dy = y - 100
        const len = Math.hypot(dx, dy) || 1
        const ux = dx / len
        const uy = dy / len
        const tx = x + ux * 10
        const ty = y + uy * 10
        return (
          <circle key={`t-${i}`} cx={tx} cy={ty} r="1.4" fill="#C084FC" />
        )
      })}

      {/* center core - abstract, not a face */}
      <circle cx="100" cy="100" r="30" fill="url(#coreGrad)" />
      <circle cx="100" cy="100" r="30" fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth="1" />
      <path
        d="M88 100h9M103 100h9M100 88v9M100 103v9"
        stroke="rgba(255,255,255,0.85)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle cx="100" cy="100" r="3.5" fill="rgba(255,255,255,0.92)" />
    </svg>
  )
}
