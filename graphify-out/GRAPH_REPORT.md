# Graph Report - obscura-dash  (2026-10-21)

## Corpus Check
- 7 files · ~1,096 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 51 nodes · 63 edges · 10 communities (5 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dc1327a6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- react
- process_image
- main
- dependencies
- scripts
- login
- scrape_category
- README.md

## God Nodes (most connected - your core abstractions)
1. `login()` - 5 edges
2. `process_image()` - 5 edges
3. `scrape_category()` - 5 edges
4. `main()` - 5 edges
5. `scripts` - 4 edges
6. `react` - 4 edges
7. `download_image()` - 4 edges
8. `upload_to_supabase_storage()` - 3 edges
9. `push_supabase()` - 3 edges
10. `react-dom` - 2 edges

## Surprising Connections (you probably didn't know these)
- `login()` --calls--> `time`  [EXTRACTED]
  superdelivery-v2.py →   _Bridges community 7 → community 8_
- `main()` --calls--> `login()`  [EXTRACTED]
  superdelivery-v2.py → superdelivery-v2.py  _Bridges community 7 → community 4_
- `scrape_category()` --calls--> `process_image()`  [EXTRACTED]
  superdelivery-v2.py → superdelivery-v2.py  _Bridges community 2 → community 8_
- `main()` --calls--> `scrape_category()`  [EXTRACTED]
  superdelivery-v2.py → superdelivery-v2.py  _Bridges community 8 → community 4_

## Import Cycles
- None detected.

## Communities (10 total, 5 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.20
Nodes (9): devDependencies, vite, @vitejs/plugin-react, name, private, type, @supabase/supabase-js, vite (+1 more)

### Community 1 - "react"
Cohesion: 0.38
Nodes (3): react, react-dom, ObscuraDashboard()

### Community 2 - "process_image"
Cohesion: 0.29
Nodes (3): download_image(), process_image(), upload_to_supabase_storage()

### Community 5 - "dependencies"
Cohesion: 0.50
Nodes (4): dependencies, react, react-dom, @supabase/supabase-js

### Community 6 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

## Knowledge Gaps
- **1 isolated node(s):** `@supabase/supabase-js`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 26 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `react` to `package.json`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **What connects `@supabase/supabase-js` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `scripts` connect `scripts` to `package.json`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `package.json`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._