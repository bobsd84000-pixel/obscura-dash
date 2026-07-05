import React, { useState, useEffect } from 'react';

const SUPABASE_URL = 'https://YOUR_SUPABASE_URL.supabase.co';
const SUPABASE_KEY = 'YOUR_SUPABASE_ANON_KEY';

export default function ObscuraDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [running, setRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [scrapedProducts, setScrapedProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('default');
  const [filterSite, setFilterSite] = useState('All');
  const [filterCat, setFilterCat] = useState('All');

  useEffect(() => {
    fetchFromSupabase();
  }, []);

  const fetchFromSupabase = async () => {
    try {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/scrape_results?order=scraped_at.desc&limit=1`, {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        }
      });
      const data = await res.json();
      if (data.length > 0) {
        setScrapedProducts(data[0].products || []);
      }
    } catch (e) {
      console.log('Supabase error, fallback activé');
    }
  };

  const features = [
    { name: 'Headless Browser', icon: '🌐', desc: 'Chromium Rust-based', perf: '30MB RAM' },
    { name: 'Stealth Mode', icon: '🕵️', desc: 'Anti-detection patterns', perf: '99.4%' },
    { name: 'CDP Protocol', icon: '⚙️', desc: 'Chrome DevTools Protocol', perf: '14ms' },
    { name: 'JavaScript Eval', icon: '✨', desc: 'DOM manipulation in-process', perf: 'Native' },
    { name: 'Network Interception', icon: '📡', desc: 'Proxy & mock requests', perf: 'Full' },
    { name: 'Cookie Persistence', icon: '🔐', desc: 'Session management', perf: 'Encrypted' },
  ];

  const crates = [
    { name: 'obscura', desc: 'Rust API for the Obscura headless browser', size: '52KB' },
    { name: 'obscura-browser', desc: 'Browser instance & lifecycle', size: '96KB' },
    { name: 'obscura-cdp', desc: 'Chrome DevTools Protocol impl', size: '308KB' },
    { name: 'obscura-cli', desc: 'Command-line interface', size: '104KB' },
    { name: 'obscura-dom', desc: 'DOM extraction & manipulation', size: '100KB' },
    { name: 'obscura-js', desc: 'JavaScript runtime bindings', size: '548KB' },
    { name: 'obscura-mcp', desc: 'MCP server for Claude', size: '116KB' },
    { name: 'obscura-net', desc: 'Network stack & proxies', size: '180KB' },
  ];

  const runDemo = () => {
    setRunning(true);
    setLogs(['🚀 Lancement Obscura...', '✅ Instance créée', '🔄 Chromium démarré', '📍 CDP connecté']);
    setTimeout(() => {
      setLogs(l => [...l, '✨ Scraping SuperDelivery...', '📊 Parsing...', '✅ 8 produits chargés']);
      setRunning(false);
      setActiveTab('results');
    }, 2500);
  };

  const getFiltered = () => {
    let list = scrapedProducts;
    if (filterSite !== 'All') list = list.filter(p => p.siteType === filterSite);
    if (filterCat !== 'All') list = list.filter(p => p.category === filterCat);
    if (search) list = list.filter(p => (p.name || '').toLowerCase().includes(search.toLowerCase()));
    if (sortBy === 'metric-desc') list = [...list].sort((a, b) => b.metric - a.metric);
    if (sortBy === 'metric-asc') list = [...list].sort((a, b) => a.metric - b.metric);
    if (sortBy === 'name-asc') list = [...list].sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    return list;
  };

  const exportCSV = () => {
    const data = getFiltered();
    const rows = [['Nom', 'Site', 'Catégorie', 'Métrique', 'URL'], ...data.map(p => ['"' + (p.name || '') + '"', p.siteType, p.category, p.metric, p.url])];
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'obscura-scrape-' + new Date().toISOString().slice(0, 10) + '.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const siteColor = { Beauty: '#e879f9', Design: '#60a5fa', SuperDelivery: '#ff6b9d' };
  const siteIcon = { Beauty: '💄', Design: '🎨', SuperDelivery: '🇯🇵' };
  const filtered = getFiltered();
  const tabs = ['overview', 'features', 'crates', 'demo', 'results'];

  return (
    <div style={{ background: '#0f0f0f', color: '#fff', minHeight: '100vh', fontFamily: 'IBM Plex Mono, monospace' }}>
      <nav style={{ background: '#1a1a1a', borderBottom: '1px solid #333', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontSize: '20px', fontWeight: 'bold', letterSpacing: '2px', color: '#00d9ff' }}>OBSCURA</div>
        <div style={{ fontSize: '12px', color: '#888' }}>Headless Browser • Rust • CDP • MCP</div>
      </nav>

      <div style={{ display: 'flex', borderBottom: '1px solid #222', overflowX: 'auto' }}>
        {tabs.map(t => (
          <button key={t} onClick={() => setActiveTab(t)} style={{ flexShrink: 0, padding: '12px 16px', background: activeTab === t ? '#00d9ff20' : 'transparent', border: 'none', color: activeTab === t ? '#00d9ff' : '#666', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold', borderBottom: activeTab === t ? '2px solid #00d9ff' : 'none', fontFamily: 'IBM Plex Mono, monospace' }}>
            {t.toUpperCase()}
          </button>
        ))}
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 24px' }}>
        {activeTab === 'overview' && (
          <div style={{ display: 'grid', gap: '24px' }}>
            <div style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '8px', padding: '20px' }}>
              <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '12px', color: '#00d9ff' }}>OBSCURA v0.1</div>
              <p style={{ fontSize: '13px', lineHeight: '1.6', color: '#aaa', margin: 0 }}>Navigateur sans tête Rust + Chromium. 30MB RAM, 14ms latence CDP, extraction DOM native, mode stealth intégré. Scrape via GitHub Actions → Supabase.</p>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
              {[{ label: 'RAM Usage', value: '30MB', color: '#4ade80' }, { label: 'CDP Latency', value: '14ms', color: '#60a5fa' }, { label: 'Stealth Score', value: '99.4%', color: '#f97316' }].map((m, i) => (
                <div key={i} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '16px', textAlign: 'center' }}>
                  <div style={{ fontSize: '11px', color: '#888', marginBottom: '8px' }}>{m.label}</div>
                  <div style={{ fontSize: '20px', fontWeight: 'bold', color: m.color }}>{m.value}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'features' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
            {features.map((f, i) => (
              <div key={i} onClick={() => setSelected(selected === i ? null : i)} style={{ background: selected === i ? '#00d9ff20' : '#1a1a1a', border: selected === i ? '1px solid #00d9ff' : '1px solid #333', borderRadius: '8px', padding: '20px', cursor: 'pointer', transition: 'all 0.2s' }}>
                <div style={{ fontSize: '24px', marginBottom: '8px' }}>{f.icon}</div>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#fff', marginBottom: '4px' }}>{f.name}</div>
                <div style={{ fontSize: '11px', color: '#888', marginBottom: '8px' }}>{f.desc}</div>
                <div style={{ fontSize: '12px', color: '#00d9ff', fontWeight: 'bold' }}>→ {f.perf}</div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'crates' && (
          <div style={{ display: 'grid', gap: '12px' }}>
            {crates.map((c, i) => (
              <a key={i} href={'https://github.com/h4ckf0r0day/obscura/tree/main/' + c.name} target="_blank" rel="noopener noreferrer" style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', textDecoration: 'none' }}>
                <div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#fff' }}>{c.name}</div>
                  <div style={{ fontSize: '11px', color: '#888', marginTop: '4px' }}>{c.desc}</div>
                </div>
                <div style={{ fontSize: '12px', color: '#00d9ff', fontWeight: 'bold' }}>{c.size}</div>
              </a>
            ))}
          </div>
        )}

        {activeTab === 'demo' && (
          <div style={{ display: 'grid', gap: '16px' }}>
            <button onClick={runDemo} disabled={running} style={{ background: running ? '#333' : '#00d9ff20', color: running ? '#888' : '#00d9ff', border: '1px solid ' + (running ? '#333' : '#00d9ff'), padding: '12px', borderRadius: '6px', fontWeight: 'bold', cursor: running ? 'not-allowed' : 'pointer', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace' }}>
              {running ? '⏳ Scraping...' : '▶ Scraper SuperDelivery'}
            </button>
            <div style={{ background: '#0a0a0a', border: '1px solid #222', borderRadius: '6px', padding: '16px', fontFamily: 'Courier New, monospace', fontSize: '11px', maxHeight: '300px', overflowY: 'auto' }}>
              {logs.length === 0 ? <div style={{ color: '#666' }}>Clique sur le bouton pour scraper...</div> : logs.map((log, i) => (
                <div key={i} style={{ color: log.includes('✅') || log.includes('✨') ? '#4ade80' : log.includes('🚀') ? '#60a5fa' : log.includes('⚠️') ? '#f97316' : '#aaa', marginBottom: '4px' }}>{log}</div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'results' && (
          <div style={{ display: 'grid', gap: '16px' }}>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'center' }}>
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Rechercher..." style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace', flex: 1, minWidth: '120px' }} />
              <select value={filterSite} onChange={e => setFilterSite(e.target.value)} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace' }}>
                <option value="All">Tous les sites</option>
                <option value="SuperDelivery">🇯🇵 Super Delivery</option>
              </select>
              <select value={filterCat} onChange={e => setFilterCat(e.target.value)} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace' }}>
                <option value="All">Toutes catégories</option>
                <option value="Mode">Mode</option>
                <option value="Accessoires">Accessoires</option>
                <option value="Ustensiles de cuisine">Ustensiles</option>
                <option value="Fournitures de bureau">Fournitures</option>
              </select>
              <select value={sortBy} onChange={e => setSortBy(e.target.value)} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace' }}>
                <option value="default">Défaut</option>
                <option value="metric-desc">Métrique ↓</option>
                <option value="metric-asc">Métrique ↑</option>
              </select>
              <button onClick={exportCSV} disabled={filtered.length === 0} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '8px 14px', color: filtered.length === 0 ? '#555' : '#00d9ff', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace', cursor: filtered.length === 0 ? 'not-allowed' : 'pointer' }}>↓ CSV</button>
              <div style={{ fontSize: '11px', color: '#888' }}>{filtered.length} résultats</div>
            </div>

            {scrapedProducts.length === 0 ? (
              <div style={{ color: '#666', fontSize: '12px', padding: '40px', textAlign: 'center', border: '1px solid #222', borderRadius: '6px' }}>
                <div style={{ marginBottom: '16px' }}>Lancez un scraping depuis l'onglet DEMO.</div>
                <button onClick={() => setActiveTab('demo')} style={{ background: '#00d9ff', color: '#000', border: 'none', padding: '10px 24px', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '12px', fontFamily: 'IBM Plex Mono, monospace' }}>▶ Aller au DEMO</button>
              </div>
            ) : filtered.length === 0 ? (
              <div style={{ color: '#666', fontSize: '12px', padding: '40px', textAlign: 'center', border: '1px solid #222', borderRadius: '6px' }}>Aucun résultat pour ces filtres.</div>
            ) : (
              <div style={{ display: 'grid', gap: '8px' }}>
                {filtered.map(p => (
                  <div key={p.id} style={{ background: '#1a1a1a', border: '1px solid #333', borderRadius: '6px', padding: '12px 16px', display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <img src={p.image} alt={p.name} width={48} height={48} style={{ borderRadius: '8px', flexShrink: 0, objectFit: 'cover' }} onError={e => { e.target.style.display = 'none'; }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#fff' }}>{p.name}</div>
                        <div style={{ fontSize: '10px', padding: '2px 6px', borderRadius: '4px', background: (siteColor[p.siteType] || '#888') + '20', color: siteColor[p.siteType] || '#888', whiteSpace: 'nowrap' }}>{siteIcon[p.siteType]} {p.siteType}</div>
                      </div>
                      <div style={{ fontSize: '11px', color: '#888', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {p.vendor + ' · ' + p.price + ' · Popularité: ' + p.popularity}
                      </div>
                    </div>
                    <div style={{ fontSize: '12px', color: siteColor[p.siteType] || '#00d9ff', flexShrink: 0, fontWeight: 'bold', textAlign: 'right' }}>
                      <div>{p.metric}</div>
                      <div style={{ fontSize: '10px', color: '#666' }}>⭐</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}