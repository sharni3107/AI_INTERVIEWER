import { useEffect, useState } from 'react'

/**
 * Tracks how far the user has scrolled through `containerRef`'s element,
 * returning a 0-1 progress value. Used to drive the Learning Journey
 * circuit/timeline animation so it moves WITH scrolling rather than
 * looping on its own. Passive scroll listener + rAF throttling only -
 * no animation library, no layout thrash. Settles (stops changing)
 * as soon as scrolling stops, and reverses smoothly on scroll up.
 */
export default function useScrollProgress(containerRef) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return

    let raf = null
    const compute = () => {
      raf = null
      const rect = el.getBoundingClientRect()
      const vh = window.innerHeight || 800
      const total = rect.height + vh * 0.55
      const scrolled = vh * 0.9 - rect.top
      const p = Math.min(1, Math.max(0, scrolled / total))
      setProgress(p)
    }
    const onScroll = () => {
      if (raf == null) raf = requestAnimationFrame(compute)
    }

    compute()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      if (raf) cancelAnimationFrame(raf)
    }
  }, [containerRef])

  return progress
}
