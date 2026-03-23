'use client'

import { useState } from 'react'
import { format, subHours } from 'date-fns'

export default function TimelineSlider() {
  const [timeOffset, setTimeOffset] = useState(0)
  const currentTime = subHours(new Date(), timeOffset)

  return (
    <div className="absolute bottom-0 left-0 right-0 bg-tactical-panel border-t border-tactical-border p-4">
      <div className="flex items-center gap-4">
        <div className="text-xs text-gray-500 w-32">
          TIMELINE
        </div>
        
        <input
          type="range"
          min="0"
          max="72"
          value={timeOffset}
          onChange={(e) => setTimeOffset(Number(e.target.value))}
          className="flex-1 h-2 bg-tactical-bg rounded-lg appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #00ff9f 0%, #00ff9f ${(timeOffset/72)*100}%, #1e2738 ${(timeOffset/72)*100}%, #1e2738 100%)`
          }}
        />
        
        <div className="text-sm font-bold text-tactical-accent w-48 text-right">
          {timeOffset === 0 ? 'LIVE' : `-${timeOffset}h`}
          <span className="text-xs text-gray-500 ml-2">
            {format(currentTime, 'MMM dd HH:mm')}
          </span>
        </div>
      </div>
    </div>
  )
}
