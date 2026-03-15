import os
import re

def enhance_city_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already enhanced
    if "Digital Nomad Hub" in content:
        return

    # Extract City and Country
    title_match = re.search(r'title: .*? (.*?) - (.*)', content)
    if not title_match:
        # Fallback to header
        header_match = re.search(r'# .*? (.*)', content)
        city = header_match.group(1).strip() if header_match else os.path.basename(filepath).replace('.md', '').capitalize()
        country = os.path.dirname(os.path.dirname(filepath)).split('/')[-1].capitalize()
    else:
        city = title_match.group(1).strip()
        country = title_match.group(2).strip()

    # Extract Price for Nomad Score
    rent_match = re.search(r'Rent \(center\) \| ([\d,]+)€', content)
    nomad_score = "⭐⭐⭐" # Default
    if rent_match:
        rent = int(rent_match.group(1).replace(',', ''))
        if rent < 700: nomad_score = "⭐⭐⭐⭐⭐"
        elif rent < 1200: nomad_score = "⭐⭐⭐⭐"
        elif rent < 1800: nomad_score = "⭐⭐⭐"
        elif rent < 2500: nomad_score = "⭐⭐"
        else: nomad_score = "⭐"

    # Generate Sections
    enhancement = f"""
## 🧭 Explore & Community

| Platform | Link |
|----------|------|
| 💬 **Reddit** | [r/{city}](https://www.reddit.com/r/{city}/) |
| 📍 **TripAdvisor** | [Things to do in {city}](https://www.tripadvisor.com/Search?q={city}) |
| 📖 **Lonely Planet** | [{city} Guide](https://www.lonelyplanet.com/search?q={city}) |

## 🚀 Digital Nomad Hub

- **Nomad Score**: {nomad_score}
- **Internet Speed**: 🛜 High Speed Fiber (Typical for {country})
- **Coworking**: [Find local workspaces](https://www.google.com/maps/search/{city}+Coworking/)
- **Best time to visit**: May - September
"""

    # Inject before ## ← Back
    if "## ← Back" in content:
        new_content = content.replace("## ← Back", enhancement + "\n## ← Back")
    else:
        new_content = content + "\n" + enhancement

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Enhanced: {city} ({country})")

def main():
    base_path = "/home/vegar/.openclaw/workspace/costofliving/europa/docs"
    for root, dirs, files in os.walk(base_path):
        if "/cities" in root:
            for file in files:
                if file.endswith(".md") and file != "alle.md":
                    enhance_city_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
