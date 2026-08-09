import React from 'react'
import ProgressBar from './ProgressBar'
import { PHASE_ICONS, PHASE_COLORS, PHASE_COLOR_HEX } from './PhaseIcons'
import '../styles/components.css'

/**
 * Renders curriculum modules/phases as a vertical timeline with a
 * scroll-linked circuit line. As `scrollProgress` (0-1) increases the
 * fill line grows downward and phase nodes activate in sequence -
 * driven purely by the caller's scroll position, not a looping
 * animation. No globe/orb graphic - the timeline itself is the
 * circuit.
 *
 * Props:
 *  - phases: [{ n, title, description, progress, startDay, endDay }]
 *  - activePhaseIndex: index of the "current" phase (gets a pulse)
 *  - scrollProgress: 0-1, how far the user has scrolled through the section
 */
export default function LearningTimeline({ phases = [], activePhaseIndex = -1, scrollProgress = 0 }) {
  const count = Math.max(1, phases.length)

  return (
    <div className="timeline">
      <div className="timeline-line" />
      <div
        className="timeline-line-fill"
        style={{ transform: `scaleY(${scrollProgress})` }}
      />
      {phases.map((phase, i) => {
        const colorKey = PHASE_COLORS[i % PHASE_COLORS.length]
        const colorHex = PHASE_COLOR_HEX[colorKey]
        const Icon = PHASE_ICONS[i % PHASE_ICONS.length]
        const isActive = i === activePhaseIndex
        const isCompleted = phase.progress >= 100
        const isLocked = !isActive && !isCompleted && phase.progress === 0 && i > activePhaseIndex
        const nodeThreshold = (i + 0.5) / count
        const isReached = scrollProgress >= nodeThreshold
        const num = String(phase.n).padStart(2, '0')

        return (
          <div
            key={phase.n}
            className="timeline-item"
            style={{ animationDelay: `${150 + i * 150}ms` }}
          >
            <div
              className={[
                'timeline-node',
                isActive ? 'active' : '',
                isCompleted ? 'completed' : '',
                isLocked ? 'locked' : '',
                isReached ? 'reached' : '',
              ].filter(Boolean).join(' ')}
              style={{ borderColor: colorHex, color: colorHex }}
            >
              <Icon width={16} height={16} strokeWidth={2} />
            </div>

            <div
              className={`timeline-card glass-card${isLocked ? ' locked' : ''}`}
              style={{ borderColor: `${colorHex}33` }}
            >
              <span className="timeline-watermark" style={{ color: `${colorHex}1F` }}>{num}</span>

              <div className="timeline-card-top">
                <div
                  className="timeline-icon-square"
                  style={{ background: `${colorHex}17`, borderColor: `${colorHex}40`, color: colorHex }}
                >
                  <Icon />
                </div>
                <div className="timeline-card-copy">
                  <span
                    className="timeline-badge"
                    style={{ background: `${colorHex}1F`, color: colorHex }}
                  >
                    Phase {phase.n}
                  </span>
                  <h4 className="timeline-title">{phase.title}</h4>
                  <p className="timeline-desc">{phase.description}</p>
                </div>
              </div>

              <ProgressBar
                value={phase.progress}
                color={colorKey === 'violet' ? 'purple' : colorKey}
                duration={900 + i * 100}
                height={7}
                showPercent
              />
            </div>
          </div>
        )
      })}
    </div>
  )
}
