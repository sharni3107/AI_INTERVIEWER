import React from 'react'

/**
 * Hand-authored outline icons matching the 4 course-phase icons shown in
 * the reference screenshots. No icon library dependency - plain inline SVG,
 * themed via `currentColor` so they inherit the phase's accent color.
 */

const common = {
  width: 22,
  height: 22,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.8,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
}

// Phase 1 - Env & Tooling
export function IconGear(props) {
  return (
    <svg {...common} {...props}>
      <circle cx="12" cy="12" r="3.2" />
      <path d="M12 2.5v2.4M12 19.1v2.4M4.2 6.3l1.9 1.4M17.9 16.3l1.9 1.4M2.5 12h2.4M19.1 12h2.4M4.2 17.7l1.9-1.4M17.9 7.7l1.9-1.4M8.3 3.9l.9 2.2M14.8 17.9l.9 2.2M3.9 15.7l2.2-.9M17.9 8.2l2.2-.9" />
    </svg>
  )
}

// Phase 2 - Data
export function IconDatabase(props) {
  return (
    <svg {...common} {...props}>
      <ellipse cx="12" cy="5.5" rx="7.5" ry="3" />
      <path d="M4.5 5.5v6c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3v-6" />
      <path d="M4.5 11.5v6c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3v-6" />
    </svg>
  )
}

// Phase 3 - Embeddings & Vector
export function IconSparkle(props) {
  return (
    <svg {...common} {...props}>
      <path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7L12 3z" />
      <path d="M19 15.5l.7 2.1 2.1.7-2.1.7-.7 2.1-.7-2.1-2.1-.7 2.1-.7.7-2.1z" />
    </svg>
  )
}

// Phase 4 - LLM & Prompting
export function IconBrain(props) {
  return (
    <svg {...common} {...props}>
      <path d="M9.5 4.5a2.5 2.5 0 00-2.5 2.5v.3a2.5 2.5 0 00-1.5 4.4 2.6 2.6 0 000 3.1A2.5 2.5 0 007 18.7v.3a2.5 2.5 0 005 0V7a2.5 2.5 0 00-2.5-2.5z" />
      <path d="M14.5 4.5A2.5 2.5 0 0117 7v.3a2.5 2.5 0 011.5 4.4 2.6 2.6 0 010 3.1A2.5 2.5 0 0117 18.7v.3a2.5 2.5 0 01-5 0V7a2.5 2.5 0 012.5-2.5z" />
      <circle cx="6.2" cy="9.5" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="17.8" cy="9.5" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="6.2" cy="15" r="0.6" fill="currentColor" stroke="none" />
      <circle cx="17.8" cy="15" r="0.6" fill="currentColor" stroke="none" />
    </svg>
  )
}

export const PHASE_ICONS = [IconGear, IconDatabase, IconSparkle, IconBrain]

// One accent per phase - cycles if there are ever more than 4 phases.
export const PHASE_COLORS = ['purple', 'blue', 'teal', 'violet']

export const PHASE_COLOR_HEX = {
  purple: '#8B5CF6',
  blue: '#3B82F6',
  teal: '#14B8A6',
  violet: '#A855F7',
}
