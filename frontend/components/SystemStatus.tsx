'use client'

import { useState, useEffect } from 'react'

export default function SystemStatus() {
  const [status, setStatus] = useState(null)
  const [showDetails, setShowDetails] = useState(false)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/system/status')
        const data = await response.json()
        setStatus(data)
      } catch (error) {
        console.error('Failed to fetch system status:', error)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 60000) // Update every minute
    return () => clearInterval(interval)
  }, [])

  if (!status) return null

  const isMockMode = status.data_sources.mode === 'mock'

  return (
    <div className="absolute top-4 right-4 z-10">
      <button
        onClick={() => setShowDetails(!showDetails)}
        className={`px-3 py-1 rounded text-xs font-mono ${
          isMockMode 
            ? 'bg-yellow-900/50 text-yellow-300 border border-yellow-600' 
            : 'bg-green-900/50 text-green-300 border border-green-600'
        }`}
      >
        {isMockMode ? '⚠ DEMO MODE' : '● LIVE DATA'}
      </button>

      {showDetails && (
        <div className="absolute right-0 mt-2 w-64 bg-tactical-panel border border-tactical-border rounded p-3 text-xs">
          <div className="font-bold mb-2 text-tactical-accent">DATA SOURCES</div>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">OpenSky Network:</span>
              <span className={status.data_sources.opensky.available ? 'text-green-400' : 'text-yellow-400'}>
                {status.data_sources.opensky.status}
              </span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-400">NASA FIRMS:</span>
              <span className={status.data_sources.nasa_firms.available ? 'text-green-400' : 'text-yellow-400'}>
                {status.data_sources.nasa_firms.status}
              </span>
            </div>
          </div>

          {isMockMode && (
            <div className="mt-3 pt-3 border-t border-tactical-border text-yellow-300">
              Using sample data for demo. Set USE_MOCK_DATA=false for live feeds.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
