'use client'

import { useState, useEffect } from 'react'
import WorldMap from '../components/WorldMap'
import TacticalSidebar from '../components/TacticalSidebar'
import TimelineSlider from '../components/TimelineSlider'
import SystemStatus from '../components/SystemStatus'

export default function Home() {
  const [aircraftData, setAircraftData] = useState(null)
  const [thermalData, setThermalData] = useState(null)
  const [sensitiveLocations, setSensitiveLocations] = useState(null)
  const [maritimeData, setMaritimeData] = useState(null)
  const [satelliteData, setSatelliteData] = useState(null)
  const [cyberData, setCyberData] = useState(null)
  const [militaryBases, setMilitaryBases] = useState(null)
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aircraft, thermal, locations, alertsData, maritime, satellites, cyber, bases] = await Promise.all([
          fetch('http://localhost:8000/api/aviation/positions').then(r => r.json()),
          fetch('http://localhost:8000/api/thermal/anomalies').then(r => r.json()),
          fetch('http://localhost:8000/api/alerts/locations').then(r => r.json()),
          fetch('http://localhost:8000/api/alerts/current').then(r => r.json()),
          fetch('http://localhost:8000/api/maritime/vessels').then(r => r.json()),
          fetch('http://localhost:8000/api/satellites/tracking').then(r => r.json()),
          fetch('http://localhost:8000/api/cyber/incidents').then(r => r.json()),
          fetch('http://localhost:8000/api/military/bases').then(r => r.json())
        ])
        
        setAircraftData(aircraft)
        setThermalData(thermal)
        setSensitiveLocations(locations)
        setMaritimeData(maritime)
        setSatelliteData(satellites)
        setCyberData(cyber)
        setMilitaryBases(bases)
        setAlerts(alertsData.alerts || [])
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
        <SystemStatus />
        <WorldMap 
          aircraftData={aircraftData}
          thermalData={thermalData}
          sensitiveLocations={sensitiveLocations}
          maritimeData={maritimeData}
          satelliteData={satelliteData}
          cyberData={cyberData}
          militaryBases={militaryBases}
        />
        <TimelineSlider />
      </div>
    </div>
  )
}
