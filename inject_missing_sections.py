import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'
MARKER = '710853'

def generate_sections(city_name, country_name):
    bk_link = f"https://tp.media/r?marker={MARKER}&p=121&u=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Fss%3D{city_name}"
    ta_link = f"https://tp.media/r?marker={MARKER}&p=125&u=https%3A%2F%2Fwww.tripadvisor.com%2FSearch%3Fq%3D{city_name}"
    lp_link = f"https://tp.media/r?marker={MARKER}&p=170&u=https%3A%2F%2Fwww.lonelyplanet.com%2Fsearch%3Fq%3D{city_name}"
    
    country_lower = country_name.lower().replace(' ', '')
    
    sections = f"""
## 🏨 Hotels & Airbnb

| Service | Link |
|---------|------|
| [Booking.com]({bk_link}) | [Hotels]({bk_link}) |
| [Airbnb](https://www.airbnb.com/s/{city_name}--{country_name}) | Vacation Rentals |

## 🧭 Explore & Community

| Platform | Link |
|----------|------|
| 💬 **Reddit** | [r/{city_name}](https://www.reddit.com/r/{city_name}/) |
| 📍 **TripAdvisor** | [Things to do in {city_name}]({ta_link}) |
| 📖 **Lonely Planet** | [{city_name} Guide]({lp_link}) |

## 🚀 Digital Nomad Hub

- **Nomad Score**: ⭐⭐⭐⭐
- **Internet Speed**: 🛜 High Speed Fiber (Typical for {country_name})
- **Coworking**: [Find local workspaces](https://www.google.com/maps/search/{city_name}+Coworking/)
- **Best time to visit**: May - September

## ← Back
[Back to {country_name} overview](../index.md)

*Data: Numbeo.com, March 2026*
"""
    return sections

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if it already has the Hotels section
    if '## 🏨 Hotels' in content or '## 🏨 Recommended Accommodation' in content:
        return False

    # Extract City and Country from H1 or Title
    match = re.search(r'^#\s*(?:🏙️\s*)?([^ \n\r]+)', content, re.MULTILINE)
    title_match = re.search(r'title:\s*(?:🏙️\s*)?[^-]+-\s*(.+)', content)
    
    if match and title_match:
        city_name = match.group(1).strip()
        country_name = title_match.group(1).strip()
        
        # Determine where to inject. Usually after the Maps Hub or "Back to Country"
        # Since these new files might end with [Back to Montenegro](../index.md), we'll replace that or append.
        
        # Remove the standalone "Back to Country" and any generic Numbeo footers if they exist loosely
        content = re.sub(r'\[Back to .*?\]\(\.\./index\.md\)\n*', '', content)
        content = re.sub(r'\*Data: Numbeo.*?$', '', content, flags=re.MULTILINE | re.DOTALL)
        
        # Append the new sections
        new_content = content.strip() + "\n" + generate_sections(city_name, country_name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
        
    return False

def run_injection():
    count = 0
    total_files = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if 'cities' in dirs:
            target_dir = os.path.join(root, 'cities')
            for f in os.listdir(target_dir):
                if f.endswith('.md'):
                    total_files += 1
                    if process_file(os.path.join(target_dir, f)):
                        count += 1
    print(f"Injection complete. Added missing sections to {count} out of {total_files} city files.")

if __name__ == "__main__":
    run_injection()
