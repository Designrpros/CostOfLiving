# GPS Coordinates for 50 European Country Centers (Approximate)
COUNTRY_COORDS = {
    "Albania": [41.15, 20.17, "albania/"],
    "Andorra": [42.50, 1.52, "andorra/"],
    "Armenia": [40.07, 45.04, "armenia/"],
    "Austria": [47.52, 14.55, "austria/"],
    "Azerbaijan": [40.14, 47.57, "azerbaijan/"],
    "Belarus": [53.71, 27.95, "belarus/"],
    "Belgium": [50.50, 4.47, "belgium/"],
    "Bosnia": [43.91, 17.67, "bosnia/"],
    "Bulgaria": [42.73, 25.48, "bulgaria/"],
    "Croatia": [45.10, 15.20, "croatia/"],
    "Cyprus": [35.12, 33.42, "cyprus/"],
    "Czechia": [49.81, 15.47, "czech/"],
    "Denmark": [56.26, 9.50, "denmark/"],
    "Estonia": [58.59, 25.01, "estonia/"],
    "Finland": [61.92, 25.74, "finland/"],
    "France": [46.22, 2.21, "france/"],
    "Georgia": [42.31, 43.35, "georgia/"],
    "Germany": [51.16, 10.45, "germany/"],
    "Greece": [39.07, 21.82, "greece/"],
    "Hungary": [47.16, 19.50, "hungary/"],
    "Iceland": [64.96, -19.02, "iceland/"],
    "Ireland": [53.41, -8.24, "ireland/"],
    "Italy": [41.87, 12.56, "italy/"],
    "Kazakhstan": [48.01, 66.92, "kazakhstan/"],
    "Latvia": [56.87, 24.60, "latvia/"],
    "Liechtenstein": [47.14, 9.52, "liechtenstein/"],
    "Lithuania": [55.17, 23.88, "lithuania/"],
    "Luxembourg": [49.81, 6.12, "luxembourg/"],
    "Malta": [35.93, 14.37, "malta/"],
    "Moldova": [47.41, 28.36, "moldova/"],
    "Monaco": [43.73, 7.42, "monaco/"],
    "Montenegro": [42.70, 19.37, "montenegro/"],
    "Netherlands": [52.13, 5.29, "netherlands/"],
    "North Macedonia": [41.60, 21.74, "north-macedonia/"],
    "Norway": [60.47, 8.46, "norway/"],
    "Poland": [51.91, 19.14, "poland/"],
    "Portugal": [39.39, -8.22, "portugal/"],
    "Romania": [45.94, 24.96, "romania/"],
    "Russia": [55.75, 37.61, "russia/"],
    "San Marino": [43.94, 12.45, "san-marino/"],
    "Serbia": [44.01, 21.00, "serbia/"],
    "Slovakia": [48.66, 19.69, "slovakia/"],
    "Slovenia": [46.15, 14.99, "slovenia/"],
    "Spain": [40.46, -3.74, "spain/"],
    "Sweden": [60.12, 18.64, "sweden/"],
    "Switzerland": [46.81, 8.22, "switzerland/"],
    "Turkey": [41.00, 28.97, "turkey/"],
    "UK": [55.37, -3.43, "uk/"],
    "Ukraine": [48.37, 31.16, "ukraine/"],
    "Vatican": [41.90, 12.45, "vatican/"]
}

def generate_map_html():
    markers_js = ""
    for name, data in COUNTRY_COORDS.items():
        markers_js += f'    L.marker([{data[0]}, {data[1]}]).addTo(map).bindPopup("<b>{name}</b><br><a href=\'{data[2]}\'>View Guide</a>");\n'

    html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    #map {{ 
        height: 500px; 
        width: 100%; 
        border-radius: 12px; 
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1;
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
    return html

if __name__ == "__main__":
    print(generate_map_html())
