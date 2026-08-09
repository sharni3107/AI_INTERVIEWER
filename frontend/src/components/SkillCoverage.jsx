import React from 'react'
import ProgressBar from './ProgressBar'
import '../styles/components.css'

/**
 * Renders topic/module performance rows.
 *
 * Props:
 *  - items: [{ label: string, value: number (0-100) }]
 */
export default function SkillCoverage({ items = [] }) {
  return (
    <div className="skill-coverage">
      {items.map((item) => (
        <ProgressBar
          key={item.label}
          label={item.label}
          value={item.value}
          color="purple"
          height={7}
        />
      ))}
    </div>
  )
}
