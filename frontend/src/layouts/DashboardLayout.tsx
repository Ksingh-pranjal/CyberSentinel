import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { Bell, BriefcaseBusiness, LayoutDashboard, LogOut, Map, Settings, UserCircle } from 'lucide-react';
import { authService } from '../services/services';

const nav = [
  ['/dashboard', 'Dashboard', LayoutDashboard],
  ['/heatmap', 'Risk Heatmap', Map],
  ['/alerts', 'Alerts', Bell],
  ['/investigations/CYB-2026-1024', 'Investigations', BriefcaseBusiness],
  ['/settings', 'Profile & Settings', Settings],
] as const;

export function DashboardLayout() {
  const u = authService.current();
  const navigate = useNavigate();
  const signOut = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <img src="/favicon.svg" alt="CyberSentinel logo" className="brand-logo" />
          <span>
            CYBER<span>SENTINEL</span>
          </span>
        </div>
        <p className="system-tag">PREDICTIVE INTELLIGENCE</p>
        <nav>
          {nav.map(([to, label, Icon]) => (
            <NavLink key={to} to={to}>
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <details className="account-menu">
          <summary className="user-card">
            <div className="avatar">{u?.name.slice(0, 1)}</div>
            <div>
              <b>{u?.name}</b>
              <small>{u?.role}</small>
            </div>
          </summary>
          <div className="account-popover">
            <button onClick={() => navigate('/settings')}>
              <UserCircle size={15} /> Account / Profile
            </button>
            <button onClick={signOut}>
              <LogOut size={15} /> Sign Out
            </button>
          </div>
        </details>
      </aside>
      <main className="main-content">
        <div className="topbar">
          <span className="live">
            <span className="live-dot" aria-hidden="true" />
            LIVE THREAT TELEMETRY
          </span>
          <button className="topbar-signout" onClick={signOut}>
            <LogOut size={15} /> Sign Out
          </button>
        </div>
        <Outlet />
      </main>
    </div>
  );
}
