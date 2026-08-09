import React, { useEffect, useRef, useState } from 'react'

/**
 * Reusable animated progress bar.
 *
 * Props:
 *  - value: number (0-100)
 *  - label: string (optional label above the bar)
 *  - color: 'purple' | 'blue' | 'teal' | 'success'
 *  - animated: boolean (default true)
 *  - duration: ms (default 900)
 *  - showPercent: boolean (default true) - renders an animated count-up number
 *  - height: px (default 8)
 */
export default function ProgressBar({
  value = 0,
  label,
  color = 'purple',
  animated = true,
  duration = 900,
  showPercent = true,
  height = 8,
}) {
  const [width, setWidth] = useState(animated ? 0 : value)
  const [count, setCount] = useState(animated ? 0 : value)
  const frameRef = useRef(null)

  useEffect(() => {
    if (!animated) {
      setWidth(value)
      setCount(value)
      return
    }

    const start = performance.now()
    const from = 0

    function tick(now) {
      const elapsed = now - start
      const t = Math.min(1, elapsed / duration)
      // ease-out cubic
      const eased = 1 - Math.pow(1 - t, 3)
      const current = from + (value - from) * eased

      setWidth(current)
      setCount(Math.round(current))

      if (t < 1) {
        frameRef.current = requestAnimationFrame(tick)
      }
    }

    frameRef.current = requestAnimationFrame(tick)

    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, animated, duration])

  const colorVar = {
    purple: 'var(--purple-400)',
    blue: 'var(--blue-500)',
    teal: 'var(--cyan-500)',
    success: 'var(--success)',
  }[color] || 'var(--purple-400)'

  return (
    <div className="progress-bar-wrap">
      {(label || showPercent) && (
        <div className="progress-bar-head">
          {label && <span className="progress-bar-label">{label}</span>}
          {showPercent && <span className="progress-bar-pct">{count}%</span>}
        </div>
      )}
      <div className="progress-bar-track" style={{ height }}>
        <div
          className="progress-bar-fill"
          style={{
            width: `${width}%`,
            background: colorVar,
          }}
        />
      </div>
    </div>
  )
}
