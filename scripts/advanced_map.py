import re
import os

BASE_DOCS = "/home/vegar/.openclaw/workspace/costofliving/europa/docs"
INDEX_PATH = os.path.join(BASE_DOCS, "index.md")

# Default coordinates if extraction fails
COUNTRY_COORDS = {
    "Albania": [41.15, 20.17], "Andorra": [42.50, 1.52], "Armenia": [40.07, 45.04],
    "Austria": [47.52, 14.55], "Azerbaijan": [40.14, 47.57], "Belarus": [53.71, 27.95],
    "Belgium": [50.50, 4.47], "Bosnia": [43.91, 17.67], "Bulgaria": [42.73, 25.48],
    "Croatia": [45.10, 15.20], "Cyprus": [35.12, 33.42], "Czechia": [49.81, 15.47],
    "Denmark": [56.26, 9.50], "Estonia": [58.59, 25.01], "Finland": [61.92, 25.74],
    "France": [46.22, 2.21], "Georgia": [42.31, 43.35], "Germany": [51.16, 10.45],
    "Greece": [39.07, 21.82], "Hungary": [47.16, 19.50], "Iceland": [64.96, -19.02],
    "Ireland": [53.41, -8.24], "Italy": [41.87, 12.56], "Kazakhstan": [48.01, 66.92],
    "Latvia": [56.87, 24.60], "Liechtenstein": [47.14, 9.52], "Lithuania": [55.17, 23.88],
    "Luxembourg": [49.81, 6.12], "Malta": [35.93, 14.37], "Moldova": [47.41, 28.36],
    "Monaco": [43.73, 7.42], "Montenegro": [42.70, 19.37], "Netherlands": [52.13, 5.29],
    "North Macedonia": [41.60, 21.74], "Norway": [60.47, 8.46], "Poland": [51.91, 19.14],
    "Portugal": [39.39, -8.22], "Romania": [45.94, 24.96], "Russia": [55.75, 37.61],
    "San Marino": [43.94, 12.45], "Serbia": [44.01, 21.00], "Slovakia": [48.66, 19.69],
    "Slovenia": [46.15, 14.99], "Spain": [40.46, -3.74], "Sweden": [60.12, 18.64],
    "Switzerland": [46.81, 8.22], "Turkey": [41.00, 28.97], "UK": [55.37, -3.43],
    "Ukraine": [48.37, 31.16], "Vatican": [41.90, 12.45]
}

def parse_rent_data():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract rent prices from the tables in index.md
    # Pattern: | 🇳🇴 [Norway](norway/) | 1,603€ | → |
    # or | 🇬🇷 [Greece](greece/) | 550€ | → |
    pattern = r"\| .* \[(.*)\]\((.*)\) \| (.*) \| → \|"
    matches = re.findall(pattern, content)
    
    data_map = {}
    for name, link, rent_str in matches:
        rent = 0
        rent_match = re.search(r"(\d+,?\d+)", rent_str)
        if rent_match:
            rent = int(rent_match.group(1).replace(",", ""))
        
        data_map[name] = {
            "link": link,
            "rent_str": rent_str,
            "rent": rent
        }
    return data_map

def get_color(rent):
    if rent == 0: return "#888" # Grey for N/A
    if rent < 800: return "#2ecc71" # Green
    if rent < 1500: return "#f1c40f" # Yellow
    return "#e74c3c" # Red

def generate_interactive_map():
    data_map = parse_rent_data()
    
    markers_js = ""
    for name, coords in COUNTRY_COORDS.items():
        info = data_map.get(name, {"link": f"{name.lower()}/", "rent_str": "N/A", "rent": 0})
        # Fix link if it doesn't end in /
        link = info["link"]
        if not link.endswith("/"): link += "/"
        
        color = get_color(info["rent"])
        markers_js += f"""
    L.circleMarker([{coords[0]}, {coords[1]}], {{
        radius: 8,
        fillColor: "{color}",
        color: "#fff",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
    }}).addTo(map)
    .bindTooltip("<b>{name}</b><br>Rent: {info['rent_str']}", {{ sticky: true }})
    .on('click', function() {{ window.location.href = '{link}'; }});
"""

    leaflet_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    #map {{ 
        height: 600px; 
        width: 100%; 
        border-radius: 12px; 
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 1;
        cursor: crosshair;
    }}
    .leaflet-tooltip {{
        background: rgba(0,0,0,0.8);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 10px;
        font-size: 14px;
    }}
</style>

<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    var map = L.map('map').setView([48.0, 15.0], 4);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }}).addTo(map);

{markers_js}
</script>
"""
    return leaflet_html

def update_index():
    map_html = generate_interactive_map()
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the old map block with the new one
    # The block starts with <link... and ends with </script>\n
    pattern = r'<link rel="stylesheet" href="https://unpkg\.com/leaflet@1\.9\.4/dist/leaflet\.css" />.*?</script>'
    new_content = re.sub(pattern, map_html, content, flags=re.DOTALL)
    
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Map updated successfully!")

if __name__ == "__main__":
    update_index()
