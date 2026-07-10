import React, { useState, useEffect } from 'react';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

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
      console.error('Fetch error:', e);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'system-ui' }}>
      <h1>Obscura Dashboard</h1>
      <p>Connected to Supabase ✓</p>
      <p>Active Tab: {activeTab}</p>
      {scrapedProducts.length > 0 && <p>Products loaded: {scrapedProducts.length}</p>}
    </div>
  );
}