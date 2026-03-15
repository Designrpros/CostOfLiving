#!/bin/bash
set -e

BASE="/home/vegar/.openclaw/workspace/costofliving/europa"
cd $BASE

echo "Creating scripts directories..."
mkdir -p scripts/archive
mkdir -p scripts/data

echo "Moving data files..."
mv data_recs_batch*.json scripts/data/ || true

echo "Moving core scripts..."
mv enhance_cities.py scripts/ || true
mv advanced_map.py scripts/ || true
mv generate_map.py scripts/ || true
mv optimize_maps.py scripts/ || true
mv inject_affiliates.py scripts/ || true
mv inject_missing_sections.py scripts/ || true
mv inject_recommendations.py scripts/ || true

echo "Moving archive scripts..."
mv finalize_naming.py scripts/archive/ || true
mv rename_praktisk.py scripts/archive/ || true
mv cleanup_praktisk.py scripts/archive/ || true
mv monetize_all.py scripts/archive/ || true
mv complete_monetization.py scripts/archive/ || true
mv final_fix_monetization.py scripts/archive/ || true
mv deep_control.py scripts/archive/ || true
mv swap_lp_to_viator.py scripts/archive/ || true
mv add_clean_lonely_planet.py scripts/archive/ || true

echo "Cleanup complete!"
