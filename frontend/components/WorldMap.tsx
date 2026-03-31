'use client'

import { useEffect, useRef } from 'react'
import Map, { Source, Layer, NavigationControl } from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'YOUR_MAPBOX_TOKEN'

export default function WorldMap({ aircraftData, thermalData, sensitiveLocations, maritimeData, satelliteData, cyberData, militaryBases }) {
  const mapRef = useRef(null)

  const aircraftLayer = {
    id: 'aircraft',
    type: 'circle',
    paint: {
      'circle-radius': 6,
      'circle-color': '#00ff9f',
      'circle-stroke-width': 2,
      'circle-stroke-color': '#0a0e1a'
    }
  }

  const thermalLayer = {
    id: 'thermal',
    type: 'circle',
    paint: {
      'circle-radius': 8,
      'circle-color': '#ff6b35',
      'circle-opacity': 0.7,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#ff0055'
    }
  }

  const sensitiveLayer = {
    id: 'sensitive',
    type: 'circle',
    paint: {
      'circle-radius': 10,
      'circle-color': '#ff0055',
      'circle-opacity': 0.3,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#ff0055'
    }
  }

  const geofenceLayer = {
    id: 'geofence',
    type: 'circle',
    paint: {
      'circle-radius': {
        stops: [
          [0, 0],
          [20, 500000]
        ],
        base: 2
      },
      'circle-color': '#ff0055',
      'circle-opacity': 0.05,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#ff0055',
      'circle-stroke-opacity': 0.3
    }
  }

  const maritimeLayer = {
    id: 'maritime',
    type: 'circle',
    paint: {
      'circle-radius': 8,
      'circle-color': '#00d4ff',
      'circle-opacity': 0.8,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#0088cc'
    }
  }

  const satelliteLayer = {
    id: 'satellite',
    type: 'circle',
    paint: {
      'circle-radius': 6,
      'circle-color': '#ffaa00',
      'circle-opacity': 0.9,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#ff6600'
    }
  }

  const cyberLayer = {
    id: 'cyber',
    type: 'circle',
    paint: {
      'circle-radius': 10,
      'circle-color': '#ff00ff',
      'circle-opacity': 0.6,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#cc00cc'
    }
  }

  const militaryBaseLayer = {
    id: 'military',
    type: 'circle',
    paint: {
      'circle-radius': 8,
      'circle-color': '#ff0000',
      'circle-opacity': 0.7,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#990000'
    }
  }

  return (
    <Map
      ref={mapRef}
      initialViewState={{
        longitude: 51.5,
        latitude: 25.3,
        zoom: 5
      }}
      style={{ width: '100%', height: '100%' }}
      mapStyle="mapbox://styles/mapbox/dark-v11"
      mapboxAccessToken={MAPBOX_TOKEN}
    >
      <NavigationControl position="top-right" />
      
      {aircraftData && (
        <Source id="aircraft-source" type="geojson" data={aircraftData}>
          <Layer {...aircraftLayer} />
        </Source>
      )}

      {thermalData && (
        <Source id="thermal-source" type="geojson" data={thermalData}>
          <Layer {...thermalLayer} />
        </Source>
      )}

      {sensitiveLocations && (
        <>
          <Source id="geofence-source" type="geojson" data={sensitiveLocations}>
            <Layer {...geofenceLayer} />
          </Source>
          <Source id="sensitive-source" type="geojson" data={sensitiveLocations}>
            <Layer {...sensitiveLayer} />
          </Source>
        </>
      )}

      {maritimeData && (
        <Source id="maritime-source" type="geojson" data={maritimeData}>
          <Layer {...maritimeLayer} />
        </Source>
      )}

      {satelliteData && (
        <Source id="satellite-source" type="geojson" data={satelliteData}>
          <Layer {...satelliteLayer} />
        </Source>
      )}

      {cyberData && (
        <Source id="cyber-source" type="geojson" data={cyberData}>
          <Layer {...cyberLayer} />
        </Source>
      )}

      {militaryBases && (
        <Source id="military-source" type="geojson" data={militaryBases}>
          <Layer {...militaryBaseLayer} />
        </Source>
      )}
    </Map>
  )
}
