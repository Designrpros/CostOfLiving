# Cost Of Living Automation Tools

This directory contains the Python scripts and JSON payloads responsible for generating, structuring, and monetizing the Cost Of Living Europe project.

## 🚀 Core Scripts

If you add new countries or cities in the future, you will run these scripts to ensure they are instantly populated with the standard template and monetized links.

| Script | Function | Usage |
|--------|----------|-------|
| `enhance_cities.py` | Populates generic content, prices, and map placeholders for newly generated city markdown files. | `python3 scripts/enhance_cities.py` |
| `inject_recommendations.py` | Reads curated JSON data from `scripts/data/` and parses hand-picked recommendations (Hotels, Activities) into specific city files. | `python3 scripts/inject_recommendations.py scripts/data/data_recs_batch1.json` |
| `inject_missing_sections.py` | Structurally appends missing Hotels, Explore, and Nomad Hub sections to any city page that lacks them. | `python3 scripts/inject_missing_sections.py` |
| `optimize_maps.py` | Refines OpenStreetMap bounding boxes for country index pages. | `python3 scripts/optimize_maps.py` |
| `advanced_map.py` | Enhances interactive Leaflet maps with dynamic markers based on cost data. | `python3 scripts/advanced_map.py` |

---

## 📂 Subdirectories

### `/data`
Stores the massive JSON payloads used by the `inject_recommendations.py` tool. These files define the exact luxury, budget, and hostel accommodations, plus the top-rated activities, for 83 major European hubs.

### `/archive`
Contains the single-use mass-migration scripts that we ran precisely once during the great site restructuring. They are preserved here in case you ever need the logic again.
Examples:
- `monetize_all.py` & `deep_control.py` (The global affiliate sweeps)
- `swap_lp_to_viator.py` & `add_clean_lonely_planet.py` (The Travelpayouts program replacement logic)
- `finalize_naming.py` (The great `byer` to `cities` rename event)

## Deployment Notes
These scripts manipulate the front-end `.md` files located in the `/docs` directory. They do NOT need to run in production. Always run them locally, perform a `git commit`, and let the GitHub Actions pipeline (`deploy.yml`) handle the final MkDocs build.
