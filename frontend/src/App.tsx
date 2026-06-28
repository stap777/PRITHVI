import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'

function App() {
  const [geoData, setGeoData] = useState<any>(null)

  useEffect(() => {
    fetch('/india_states.geojson')
      .then((res) => res.json())
      .then((data) => setGeoData(data))
  }, [])

  const defaultStyle = {
    color: '#2563eb',
    weight: 1,
    fillColor: '#93c5fd',
    fillOpacity: 0.3
  }

  const onEachFeature = (feature: any, layer: any) => {
    layer.bindPopup(feature.properties.shapeName)

    layer.on({
      click: () => {
        // reset all styles
        layer._map.eachLayer((l: any) => {
          if (l.feature) {
            l.setStyle(defaultStyle)
          }
        })

        // highlight selected state
        layer.setStyle({
          fillColor: 'yellow',
          fillOpacity: 0.7,
          color: 'black',
          weight: 2
        })
      }
    })
  }

  return (
    <MapContainer
      center={[22.5, 79]}
      zoom={5}
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {geoData && (
        <GeoJSON
          data={geoData}
          onEachFeature={onEachFeature}
          style={defaultStyle}
        />
      )}
    </MapContainer>
  )
}

export default App