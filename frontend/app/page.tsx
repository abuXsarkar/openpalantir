'use client'

import { useState, useEffect } from 'react'
import WorldMap from '../components/WorldMap'
import TacticalSidebar from '../components/TacticalSidebar'
import TimelineSlider from '../components/TimelineSlider'

export default function Home() {
  const [aircraftData, setAircraftData] = useState(null)
  const [thermalData, setThermalData] = useState(null)
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aircraft, thermal] = await Promise.all([
          fetch('http://localhost:8000/api/aviation/positions').then(r => r.json()),
          fetch('http://localhost:8000/api/thermal/anomalies').then(r => r.json())
        ])
        
        setAircraftData(aircraft)
        setThermalData(thermal)
        
        // Generate alerts
        const newAlerts = []
        if (aircraft.features) {
          aircraft.features.forEach(f => {
            if (f.properties.callsign?.includes('RCH') || f.properties.callsign?.includes('CNV')) {
              newAlerts.push({
                type: 'military',
                message: `Military aircraft detected: ${f.properties.callsign}`,
                location: f.properties.country,
                time: new Date()
              })
            }
          })
        }
        setAlerts(newAlerts)
      } catch (error) {
        console.error('Data fetch error:', error)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="h-screen w-screen flex">
      <TacticalSidebar alerts={alerts} />
      <div className="flex-1 relative">
        <WorldMap 
          aircraftData={aircraftData}
          thermalData={thermalData}
        />
        <TimelineSlider />
      </div>
    </div>
  )
}
