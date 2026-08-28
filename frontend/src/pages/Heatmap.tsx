import { useEffect, useMemo, useState } from 'react';
import { Filter, RefreshCw, X } from 'lucide-react';
import { predictionService } from '../services/services';
import type { Filters, Prediction } from '../types';
import { MapView } from '../components/MapView';
import { Empty, Loading, PageHeader, RiskBadge, ErrorState } from '../components/ui';
import { useNavigate } from 'react-router-dom';

const blank: Filters = { region: '', category: '', window: '', risk: '' };

export function Heatmap() {
  const [all, setAll] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>(blank);
  const [selected, setSelected] = useState<Prediction>();
  const nav = useNavigate();

  const fetchPredictions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictionService.list();
      setAll(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch predictions from server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  const data = useMemo(
    () =>
      all.filter(
        (p) =>
          (!filters.region || p.region === filters.region) &&
          (!filters.category || p.crime_category === filters.category) &&
          (!filters.window || p.predicted_window === filters.window) &&
          (!filters.risk || p.risk_level === filters.risk)
      ),
    [all, filters]
  );

  const options = (key: keyof Filters) => [
    ...new Set(
      all.map((p) =>
        key === 'category'
          ? p.crime_category
          : key === 'window'
          ? p.predicted_window
          : key === 'region'
          ? p.region
          : p.risk_level
      )
    ),
  ].filter(Boolean);

  const set = (key: keyof Filters, value: string) =>
    setFilters((f) => ({ ...f, [key]: value }));

  if (loading) return <Loading />;
  if (error) {
    return (
      <div className="page">
        <PageHeader eyebrow="GIS INTELLIGENCE" title="Risk heatmap" />
        <ErrorState>
          {error}
          <div style={{ marginTop: '1rem' }}>
            <button className="btn secondary" onClick={fetchPredictions}>
              <RefreshCw size={16} /> Retry
            </button>
          </div>
        </ErrorState>
      </div>
    );
  }

  return (
    <div className="page">
      <PageHeader eyebrow="GIS INTELLIGENCE" title="Risk heatmap">
        <button
          className="btn secondary"
          onClick={() => {
            setFilters(blank);
            setSelected(undefined);
          }}
        >
          <RefreshCw size={16} /> Reset operational view
        </button>
      </PageHeader>
      <p className="demo-banner">
        Live GIS Predictive Threat Forecasting. Markers represent ML risk scores across monitored bank and ATM clusters.
      </p>
      <div className="filters">
        <Filter size={17} />
        {(['region', 'category', 'window', 'risk'] as const).map((k) => (
          <label key={k}>
            <span>
              {k === 'category'
                ? 'Crime type'
                : k === 'window'
                ? 'Time window'
                : k === 'risk'
                ? 'Risk level'
                : 'Region'}
            </span>
            <select
              value={filters[k]}
              onChange={(e) => set(k, e.target.value)}
            >
              <option value="">
                All{' '}
                {k === 'risk'
                  ? 'levels'
                  : k === 'window'
                  ? 'windows'
                  : k === 'category'
                  ? 'crime types'
                  : 'regions'}
              </option>
              {options(k).map((x) => (
                <option key={x} value={x}>{x}</option>
              ))}
            </select>
          </label>
        ))}
        <button className="clear" onClick={() => setFilters(blank)}>
          <X size={15} /> Clear
        </button>
      </div>

      <div className="heatmap-layout">
        <section className="panel map-panel full">
          <MapView
            data={data}
            selected={selected?.id}
            onSelect={setSelected}
          />
          <div className="legend">
            {(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'] as const).map((x) => (
              <RiskBadge key={x} level={x} />
            ))}
          </div>
        </section>
        <aside className="intel-sidebar">
          {selected ? (
            <>
              <p className="eyebrow">SELECTED LOCATION</p>
              <h2>{selected.location_id}</h2>
              <p>
                {selected.location_name}
                <br />
                {selected.region}
              </p>
              <div className="score">
                <strong>{selected.risk_score}</strong>
                <span>/100 risk score</span>
              </div>
              <RiskBadge level={selected.risk_level} />
              <dl>
                <div>
                  <dt>Predicted window</dt>
                  <dd>{selected.predicted_window}</dd>
                </div>
                <div>
                  <dt>Crime category</dt>
                  <dd>{selected.crime_category}</dd>
                </div>
                <div>
                  <dt>Confidence</dt>
                  <dd>{selected.confidence}%</dd>
                </div>
              </dl>
              <button
                className="btn"
                onClick={() => nav(`/predictions/${selected.id}`)}
              >
                View details
              </button>
            </>
          ) : data.length === 0 ? (
            <Empty>No predictions found matching the selected filters.</Empty>
          ) : (
            <Empty>Select a map marker or item to inspect prediction intelligence.</Empty>
          )}
          <p className="result-count">{data.length} locations shown</p>
        </aside>
      </div>
    </div>
  );
}
