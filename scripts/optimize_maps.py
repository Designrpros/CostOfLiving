import os
import re

BASE_DOCS = "/home/vegar/.openclaw/workspace/costofliving/europa/docs"

def get_meta(content):
    title_match = re.search(r'title: (?:🏙️ )?(.*)', content)
    title = title_match.group(1).split(" - ")[0].strip() if title_match else "this location"
    return title

def tighten_osm(bbox):
    # bbox format: left,bottom,right,top (west, south, east, north)
    # Example: 4.0%2C58.0%2C16.0%2C71.0
    try:
        parts = [float(p) for p in bbox.split('%2C')]
        if len(parts) != 4: return bbox
        
        # Calculate center
        lon_c = (parts[0] + parts[2]) / 2
        lat_c = (parts[1] + parts[3]) / 2
        
        # Tighten by reduction (e.g. show 60% of original span)
        lon_span = (parts[2] - parts[0]) * 0.6
        lat_span = (parts[3] - parts[1]) * 0.6
        
        # Minimum spans to avoid being TOO zoomed in for small countries
        lon_span = max(lon_span, 2.0)
        lat_span = max(lat_span, 2.0)
        
        new_bbox = f"{lon_c - lon_span/2:.2f}%2C{lat_c - lat_span/2:.2f}%2C{lon_c + lon_span/2:.2f}%2C{lat_c + lat_span/2:.2f}"
        return new_bbox
    except:
        return bbox

def process_file(filepath, country_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    is_index = filepath.endswith("index.md")
    location_name = get_meta(content)

    # 1. Update Country Index (OSM)
    if is_index and "praktisk" not in filepath and "backpack" not in filepath:
        osm_pattern = r'src="https://www.openstreetmap.org/export/embed.html\?bbox=([^&"]+)&layer=mapnik"'
        match = re.search(osm_pattern, content)
        if match:
            old_bbox = match.group(1)
            new_bbox = tighten_osm(old_bbox)
            content = content.replace(old_bbox, new_bbox)

    # 2. Update City Pages (Switch to Google Maps Embed for better auto-zoom)
    elif "/cities/" in filepath:
        # Check for existing iframe (OSM or Google)
        iframe_pattern = r'<iframe.*</iframe>'
        google_embed = f'<iframe width="100%" height="300" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q={location_name.replace(" ", "+")},{country_name.replace(" ", "+")}&t=&z=12&ie=UTF8&iwloc=&output=embed"></iframe>'
        
        if re.search(iframe_pattern, content):
            content = re.sub(iframe_pattern, google_embed, content)
        else:
            # Inject after H1 if missing
            content = re.sub(r'(^# .*)\n', r'\1\n\n' + google_embed + '\n', content, count=1, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("--- Running Map Zoom Optimization ---")
    files_updated = 0
    for root, dirs, files in os.walk(BASE_DOCS):
        # Determine country name from folder
        rel_path = os.path.relpath(root, BASE_DOCS)
        parts = rel_path.split(os.sep)
        if not parts or parts[0] == '.': continue
        country_name = parts[0].capitalize()
        
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                process_file(filepath, country_name)
                files_updated += 1
                
    print(f"Done! Optimized maps in {files_updated} files.")

if __name__ == "__main__":
    main()
