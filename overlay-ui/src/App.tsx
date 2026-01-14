import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './index.css'

interface Detection {
  x: number
  y: number
  w: number
  h: number
  conf: number
  detected: boolean
}

function App() {
  const [target, setTarget] = useState<Detection | null>(null)
  const [connected, setConnected] = useState(false)
  const [combatMode, setCombatMode] = useState(false)

  useEffect(() => {
    // Connect to Python Backend
    const connect = () => {
      const ws = new WebSocket('ws://localhost:8000/ws')

      ws.onopen = () => {
        setConnected(true)
        console.log("Connected to Vision Engine")
      }

      ws.onclose = () => {
        setConnected(false)
        console.log("Disconnected... retrying")
        setTimeout(connect, 1000)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          // data format: { detected: boolean, x, y, w, h, conf }
          // Sync Combat State
          if (data.combat_enabled !== undefined) setCombatMode(data.combat_enabled)

          if (data.detected) {
            setTarget(data)
          } else {
            setTarget(null)
          }
        } catch (e) {
          console.error(e)
        }
      }
    }
    connect()
  }, [])

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      position: 'relative',
      background: 'transparent'
    }}>

      {/* 
        Glassmorphic Status HUD (Top Center) 
        - Liquid Glass Effect: backdrop-filter + semi-transparent white/black
      */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '15px',
        alignItems: 'center',
        padding: '10px 25px',
        borderRadius: '20px',
        background: 'rgba(20, 20, 20, 0.4)', // Dark glass base
        backdropFilter: 'blur(12px)',         // The "Liquid" blur
        border: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)'
      }}>
        {/* Status Dot */}
        <div style={{
          width: 10, height: 10, borderRadius: '50%',
          background: connected ? '#00ff88' : '#ff0055',
          boxShadow: connected ? '0 0 10px #00ff88' : '0 0 10px #ff0055'
        }} />

        <span style={{
          fontFamily: '"SF Pro Display", "Inter", sans-serif',
          color: 'rgba(255, 255, 255, 0.9)',
          fontSize: '14px',
          fontWeight: 600,
          letterSpacing: '0.5px'
        }}>
          {connected ? 'VISION ENGINE: ONLINE' : 'SEARCHING FOR ENGINE...'}
        </span>

        {/* Divider */}
        <div style={{ width: 1, height: 16, background: 'rgba(255,255,255,0.2)' }} />

        {/* Combat Status */}
        <span style={{
          fontFamily: '"SF Pro Display", "Inter", sans-serif',
          color: combatMode ? '#ff0055' : 'rgba(255, 255, 255, 0.5)',
          fontSize: '14px',
          fontWeight: 600,
          letterSpacing: '0.5px'
        }}>
          {combatMode ? 'COMBAT: ON' : 'COMBAT: OFF'}
        </span>
      </div>

      {/* Target Box Animation */}
      <AnimatePresence>
        {target && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{
              opacity: 1,
              scale: 1,
              x: target.x,
              y: target.y,
              width: target.w,
              height: target.h
            }}
            exit={{ opacity: 0, scale: 1.1, filter: "blur(20px)" }}
            transition={{
              type: "spring",
              stiffness: 500,
              damping: 20,
              mass: 0.8
            }}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              // Liquid Border
              border: '2px solid rgba(0, 255, 136, 0.6)',
              borderRadius: '12px',
              // Inner Glow
              boxShadow: 'inset 0 0 20px rgba(0, 255, 136, 0.2), 0 0 15px rgba(0, 255, 136, 0.4)',
              // Glass fill
              background: 'rgba(0, 255, 136, 0.05)',
              backdropFilter: 'blur(2px)'
            }}
          >
            {/* Header / Confidence Tag */}
            <div style={{
              position: 'absolute',
              top: -30,
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'rgba(0, 0, 0, 0.6)',
              backdropFilter: 'blur(4px)',
              border: '1px solid rgba(0, 255, 136, 0.3)',
              borderRadius: '8px',
              padding: '4px 12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              minWidth: '80px'
            }}>
              <span style={{
                color: '#00ff88',
                fontFamily: 'monospace',
                fontSize: 12,
                fontWeight: 'bold',
                textShadow: '0 0 10px rgba(0, 255, 136, 0.5)'
              }}>
                {(target.conf * 100).toFixed(0)}% LOCK
              </span>
            </div>

            {/* Decorative Corners */}
            <Corner style={{ top: -2, left: -2, borderTop: '3px solid #fff', borderLeft: '3px solid #fff' }} />
            <Corner style={{ top: -2, right: -2, borderTop: '3px solid #fff', borderRight: '3px solid #fff' }} />
            <Corner style={{ bottom: -2, left: -2, borderBottom: '3px solid #fff', borderLeft: '3px solid #fff' }} />
            <Corner style={{ bottom: -2, right: -2, borderBottom: '3px solid #fff', borderRight: '3px solid #fff' }} />

          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Helper for corners
const Corner = ({ style }: { style: React.CSSProperties }) => (
  <div style={{
    position: 'absolute',
    width: 8,
    height: 8,
    borderRadius: '2px',
    borderColor: 'rgba(255, 255, 255, 0.8)',
    ...style
  }} />
)

export default App
