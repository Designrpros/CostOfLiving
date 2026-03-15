import os
import json
import re
import urllib.parse

MARKER = "710853"
BASE_DOCS = "/home/vegar/.openclaw/workspace/costofliving/europa/docs"
P_BOOKING = "121"
P_TRIPADVISOR = "125"

def monetize_booking(query):
    encoded = urllib.parse.quote(query)
    return f"https://tp.media/r?marker={MARKER}&p={P_BOOKING}&u=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Fss%3D{encoded}"

def monetize_ta(query):
    encoded = urllib.parse.quote(query)
    return f"https://tp.media/r?marker={MARKER}&p={P_TRIPADVISOR}&u=https%3A%2F%2Fwww.tripadvisor.com%2FSearch%3Fq%3D{encoded}"

def update_city_file(filepath, city_id, data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Hotels Section
    hotel_lines = [
        "## 🏨 Recommended Accommodation",
        f"- **Luxury**: [{data['luxury']['name']}]({monetize_booking(data['luxury']['name'] + ' ' + city_id)}) — {data['luxury']['desc']}",
        f"- **Budget**: [{data['budget']['name']}]({monetize_booking(data['budget']['name'] + ' ' + city_id)}) — {data['budget']['desc']}",
        f"- **Hostel**: [{data['hostel']['name']}]({monetize_booking(data['hostel']['name'] + ' ' + city_id)}) — {data['hostel']['desc']}"
    ]
    hotel_block = "\n".join(hotel_lines)
    
    # Replace the old table
    content = re.sub(r'## 🏨 Hotels & Airbnb.*?\n\n|## 🏨 Hotels & Airbnb.*?$', hotel_block + "\n\n", content, flags=re.DOTALL)
    
    # 2. Update Explore Section
    explore_lines = [
        "## 🧭 Explore & Community",
        f"- **Top Activity**: [{data['activity']['name']}]({monetize_ta(data['activity']['name'] + ' ' + city_id)}) — {data['activity']['desc']}",
        f"- **Social**: [Find {city_id} on Reddit](https://www.reddit.com/r/{city_id.replace(' ', '')}/)",
        f"- **Guide**: [Lonely Planet {city_id}](https://www.lonelyplanet.com/search?q={urllib.parse.quote(city_id)})"
    ]
    explore_block = "\n".join(explore_lines)
    
    # Replace the old table
    content = re.sub(r'## 🧭 Explore & Community.*?\n\n|## 🧭 Explore & Community.*?$', explore_block + "\n\n", content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 inject_recommendations.py <data_file.json>")
        return
        
    data_file = sys.argv[1]
    with open(data_file, 'r') as f:
        recs = json.load(f)
    
    print(f"--- Injecting Recommendations ({data_file}) ---")
    files_updated = 0
    
    for root, dirs, files in os.walk(BASE_DOCS):
        for file in files:
            city_name = file.replace(".md", "").capitalize()
            # Handle special cases or matching
            match = None
            for key in recs:
                if key.lower() == city_name.lower():
                    match = key
                    break
            
            if match:
                filepath = os.path.join(root, file)
                print(f"Updating {match} ({filepath})")
                update_city_file(filepath, match, recs[match])
                files_updated += 1
                
    print(f"Done! Updated recommendations in {files_updated} files.")

if __name__ == "__main__":
    main()
