import os
import re
import urllib.parse

MARKER = "710853"
BASE_DOCS = "/home/vegar/.openclaw/workspace/costofliving/europa/docs"

# Travelpayouts Program IDs
P_BOOKING = "121"
P_TRIPADVISOR = "125"

def get_location_name(content):
    # Try to get city name from H1
    h1_match = re.search(r'^# (?:🏙️ )?(.*)', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return None

def monetize_links(content, location_name):
    if not location_name:
        return content
    
    encoded_name = urllib.parse.quote(location_name)
    
    # 1. Booking.com replacement
    # Pattern: [Booking.com](https://www.booking.com/searchresults.html?ss=CityName)
    booking_pattern = r'\[Booking\.com\]\(https://www\.booking\.com/searchresults\.html\?ss=.*?\)'
    booking_aff = f'[Booking.com](https://tp.media/r?marker={MARKER}&p={P_BOOKING}&u=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Fss%3D{encoded_name})'
    content = re.sub(booking_pattern, booking_aff, content)
    
    # 2. TripAdvisor replacement
    # Pattern: [TripAdvisor](https://www.tripadvisor.com/Search?q=CityName)
    ta_pattern = r'\[TripAdvisor\]\(https://www\.tripadvisor\.com/Search\?q=.*?\)'
    ta_aff = f'[TripAdvisor](https://tp.media/r?marker={MARKER}&p={P_TRIPADVISOR}&u=https%3A%2F%2Fwww.tripadvisor.com%2FSearch%3Fq%3D{encoded_name})'
    content = re.sub(ta_pattern, ta_aff, content)
    
    return content

def main():
    print(f"--- Monetizing Site with Travelpayouts (Marker: {MARKER}) ---")
    files_updated = 0
    
    for root, dirs, files in os.walk(BASE_DOCS):
        for file in files:
            if file.endswith(".md") and file != "index.md": # Skip main index, mostly country/city pages
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                location_name = get_location_name(content)
                if not location_name:
                    continue
                
                new_content = monetize_links(content, location_name)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_updated += 1
    
    print(f"Done! Updated affiliates in {files_updated} files.")

if __name__ == "__main__":
    main()
