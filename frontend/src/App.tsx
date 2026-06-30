import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'

function App() {
  const [geoData, setGeoData] = useState<any>(null)
  const [layerType, setLayerType] = useState('rainfall')

  useEffect(() => {
    fetch('/india_states.geojson')
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.log(err))
  }, [])

  // Climate data (your manual data kept)
  const climateData: any = {
    Maharashtra: { rainfall: 250, temp: 34 },
    Gujarat: { rainfall: 120, temp: 39 },
    Rajasthan: { rainfall: 60, temp: 43 },
    Kerala: { rainfall: 420, temp: 40 },
    Karnataka: { rainfall: 180, temp: 32 },
    Delhi: { rainfall: 90, temp: 41 },
    "Tamil Nadu": { rainfall: 140, temp: 36 },
    Odisha: { rainfall: 280, temp: 33 },
    Punjab: { rainfall: 70, temp: 40 },
    Haryana: { rainfall: 120, temp: 38 },
    "West Bengal": { rainfall: 300, temp: 31 },
    Chhattisgarh: { rainfall: 100, temp: 42 },
    Bihar: { rainfall: 100, temp: 41 },
    Jharkhand: { rainfall: 110, temp: 39 },
    Goa: { rainfall: 150, temp: 38 },
    Tripura: { rainfall: 100, temp: 41 },
    Meghalaya: { rainfall: 170, temp: 31 },
    Mizoram: { rainfall: 120, temp: 41 },
    Nagaland: { rainfall: 90, temp: 41 },
    Sikkim: { rainfall: 90, temp: 20 },
    "Arunachal Pradesh": { rainfall: 90, temp: 41 },
    Manipur: { rainfall: 90, temp: 41 },
    Uttarakhand: { rainfall: 110, temp: 25 },
    Assam: { rainfall: 95, temp: 34 },
    "Madhya Pradesh": { rainfall: 160, temp: 37 },
    "Uttar Pradesh": { rainfall: 200, temp: 37 },
    Ladakh: { rainfall: 70, temp: 11 },
    Telangana: { rainfall: 100, temp: 38 },
    "Andhra Pradesh": { rainfall: 200, temp: 35 },
    "Himachal Pradesh": { rainfall: 60, temp: 23 },
    "Jammu and Kashmir": { rainfall: 30, temp: 15 },
    "Andaman and Nicobar Islands": { rainfall: 10, temp: 25 },
    Lakshadweep: { rainfall: 10, temp: 28 }
  }

  const getColor = (stateName: string) => {
    const cleanName = stateName
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")

    const data = climateData[cleanName]

    if (!data) return "#d1d5db"

    if (layerType === "rainfall") {
      const rain = data.rainfall
      if (rain > 300) return "#08306b"
      if (rain > 200) return "#2171b5"
      if (rain > 100) return "#6baed6"
      return "#deebf7"
    }

    if (layerType === "temperature") {
      const temp = data.temp
      if (temp > 40) return "#7f0000"
      if (temp > 35) return "#ef4444"
      if (temp > 30) return "#fca5a5"
      return "#fee2e2"
    }

    if (layerType === "heatmap") {
      const temp = data.temp
      const rain = data.rainfall
      if (temp > 40 || rain > 350) return "#b91c1c"
      if (temp > 35 || rain > 200) return "#f97316"
      return "#22c55e"
    }

    return "#93c5fd"
  }

  const getRisk = (temp: number, rain: number) => {
    if (temp > 40 || rain > 350) return "High"
    if (temp > 35 || rain > 200) return "Moderate"
    return "Low"
  }

  const styleFeature = (feature: any) => {
    const stateName = feature.properties.shapeName

    return {
      fillColor: getColor(stateName),
      color: 'black',
      weight: 1,
      fillOpacity: 0.6
    }
  }

  const onEachFeature = (feature: any, layer: any) => {
    const stateName = feature.properties.shapeName

    const cleanName = stateName
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")

    const data = climateData[cleanName]

    if (data) {
      const risk = getRisk(data.temp, data.rainfall)

      layer.bindTooltip(
        `
        <strong>${stateName}</strong><br/>
        Rainfall: ${data.rainfall} mm<br/>
        Temperature: ${data.temp} °C<br/>
        Risk: ${risk}<br/>
        `,
        {
          sticky: true,
          direction: "top"
        }
      )
    } else {
      layer.bindTooltip(stateName, {
        sticky: true,
        direction: "top"
      })
    }

    layer.bindPopup(stateName)

    layer.on({
      click: () => {
        // reset all styles
        layer._map.eachLayer((l: any) => {
          if (l.feature) {
            l.setStyle(styleFeature(l.feature))
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
    <div style={{ position: 'relative' }}>
      <div
        style={{
          position: 'absolute',
          top: '70px',
          left: '20px',
          zIndex: 1000,
          background: 'white',
          padding: '8px',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
        }}
      >
        <select
          value={layerType}
          onChange={(e) => setLayerType(e.target.value)}
        >
          <option value="rainfall">Rainfall Layer</option>
          <option value="temperature">Temperature Layer</option>
          <option value="heatmap">Heatmap Layer</option>
        </select>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          background: '#1e293b',
          color: 'white',
          padding: '12px',
          borderRadius: '8px',
          zIndex: 1000,
          fontSize: '14px',
          minWidth: '200px'
        }}
      >
        <strong>Climate Legend</strong>

        {layerType === 'rainfall' && (
          <>
            <div>🔵 Dark Blue → Heavy Rain</div>
            <div>🔷 Blue → Medium Rain</div>
            <div>⚪ Light Blue → Low Rain</div>
          </>
        )}

        {layerType === 'temperature' && (
          <>
            <div>🔴 Dark Red → Extreme Heat</div>
            <div>🟥 Red → High Temp</div>
            <div>🌸 Pink → Moderate Temp</div>
          </>
        )}

        {layerType === 'heatmap' && (
          <>
            <div>🔴 Red → High Climate Risk</div>
            <div>🟠 Orange → Moderate Risk</div>
            <div>🟢 Green → Safe Zone</div>
          </>
        )}
      </div>

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
            key={layerType}
            data={geoData}
            onEachFeature={onEachFeature}
            style={styleFeature}
          />
        )}
      </MapContainer>
    </div>
  )
}

export default App