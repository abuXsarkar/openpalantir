'use client'

import { useEffect, useRef } from 'react'
import Map, { Source, Layer, NavigationControl } from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = 'YOUR_MAPBOX_TOKEN'

export default function WorldMap({ aircraftData, thermalData }) {
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
    </Map>
  )
}
