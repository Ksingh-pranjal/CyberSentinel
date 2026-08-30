import { useEffect } from 'react';
import L from 'leaflet';
import { MapContainer, Marker, Popup, TileLayer, Tooltip, useMap } from 'react-leaflet';
import type { Prediction } from '../types';
import { riskColor } from '../utils/risk';

function Fit({ data }: { data: Prediction[] }) {
  const map = useMap();

  useEffect(() => {
    if (data.length) {
      map.fitBounds(data.map((p) => [p.latitude, p.longitude]), {
        padding: [35, 35],
        maxZoom: 11,
      });
    }
  }, [data, map]);

  return null;
}

function markerIcon(prediction: Prediction, selected?: string) {
  const color = riskColor(prediction.risk_level);
  const elevated = prediction.risk_level === 'CRITICAL' || prediction.risk_level === 'HIGH';

  return L.divIcon({
    className: '',
    html: `<div class="map-pin ${selected === prediction.id ? 'selected' : ''} ${elevated ? 'elevated-risk' : ''}" style="--pin:${color}"><span></span></div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -12],
  });
}

export function MapView({
  data,
  onSelect,
  selected,
  compact = false,
}: {
  data: Prediction[];
  onSelect: (p: Prediction) => void;
  selected?: string;
  compact?: boolean;
}) {
  return (
    <div className={`map ${compact ? 'compact' : ''}`}>
      <MapContainer center={[17.3, 80.2]} zoom={6} scrollWheelZoom>
        <TileLayer
          attribution="&copy; OpenStreetMap contributors &copy; CARTO"
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        <Fit data={data} />
        {data.map((p) => (
          <Marker
            key={p.id}
            position={[p.latitude, p.longitude]}
            eventHandlers={{ click: () => onSelect(p) }}
            icon={markerIcon(p, selected)}
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={0.96}>
              {p.location_id} · {p.risk_level} · {p.risk_score}/100
            </Tooltip>
            <Popup>
              <div className="map-popup">
                <p className="eyebrow">PREDICTIVE RISK NODE</p>
                <strong>{p.location_name}</strong>
                <span>{p.location_id} · {p.region}</span>
                <dl>
                  <div>
                    <dt>Risk level</dt>
                    <dd>{p.risk_level}</dd>
                  </div>
                  <div>
                    <dt>Risk score</dt>
                    <dd>{p.risk_score}/100</dd>
                  </div>
                  <div>
                    <dt>Predicted window</dt>
                    <dd>{p.predicted_window}</dd>
                  </div>
                  <div>
                    <dt>Confidence</dt>
                    <dd>{p.confidence}%</dd>
                  </div>
                </dl>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
