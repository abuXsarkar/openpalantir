'use client'

import { format } from 'date-fns'

export default function TacticalSidebar({ alerts }) {
  return (
    <div className="w-96 bg-tactical-panel border-r border-tactical-border flex flex-col">
      <div className="p-6 border-b border-tactical-border">
        <h1 className="text-2xl font-bold text-tactical-accent tracking-wider">
          GEOINT PORTAL
        </h1>
        <p className="text-xs text-gray-500 mt-1">SIGNAL-TO-MAP INTELLIGENCE</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        <div className="bg-tactical-bg rounded p-3 border border-tactical-border">
          <div className="text-xs text-gray-500 mb-2">ACTIVE ALERTS</div>
          <div className="text-2xl font-bold text-tactical-accent">
            {alerts.length}
          </div>
        </div>

        <div className="space-y-2">
          {alerts.length === 0 ? (
            <div className="text-sm text-gray-500 text-center py-8">
              No active alerts
            </div>
          ) : (
            alerts.map((alert, idx) => (
              <div 
                key={idx}
                className="bg-tactical-bg rounded p-3 border-l-4 border-tactical-warning"
              >
                <div className="flex items-start justify-between mb-1">
                  <span className="text-xs font-bold text-tactical-warning uppercase">
                    {alert.type}
                  </span>
                  <span className="text-xs text-gray-500">
                    {format(alert.time, 'HH:mm:ss')}
                  </span>
                </div>
                <div className="text-sm">{alert.message}</div>
                <div className="text-xs text-gray-500 mt-1">{alert.location}</div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="p-4 border-t border-tactical-border">
        <div className="grid grid-cols-3 gap-2 text-center">
          <div className="bg-tactical-bg rounded p-2">
            <div className="text-xs text-gray-500">AVIATION</div>
            <div className="text-lg font-bold text-tactical-accent">●</div>
          </div>
          <div className="bg-tactical-bg rounded p-2">
            <div className="text-xs text-gray-500">MARITIME</div>
            <div className="text-lg font-bold text-gray-600">●</div>
          </div>
          <div className="bg-tactical-bg rounded p-2">
            <div className="text-xs text-gray-500">THERMAL</div>
            <div className="text-lg font-bold text-gray-600">●</div>
          </div>
        </div>
      </div>
    </div>
  )
}
