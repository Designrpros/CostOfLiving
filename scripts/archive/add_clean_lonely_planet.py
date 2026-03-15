import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'

def re_add_lonely_planet(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Check if we already have Lonely Planet
    if '📖 Lonely Planet' in content or 'Lonely Planet' in content:
        # Check if it's the affiliate one we just removed or a new one
        if 'tp.media/r' not in content.split('Lonely Planet')[0] and 'tp.media/r' not in content:
            # We already have it, maybe it wasn't replaced
            return False

    match = re.search(r'^#\s*(?:🏙️\s*)?([^ \n\r]+)', content, re.MULTILINE)
    if not match: return False
    city_name = match.group(1).strip()
    
    # The clean, non-affiliate Lonely Planet Search link
    lp_clean_link = f"https://www.lonelyplanet.com/search?q={city_name}"
    lp_row = f"| 📖 **Lonely Planet** | [{city_name} Guide]({lp_clean_link}) |\n"

    # We need to find the Explore & Community table and append to it.
    explore_section = re.search(r'(## 🧭 Explore & Community.*?(?=\n## |\Z))', content, re.DOTALL)
    if explore_section:
        block = explore_section.group(1)
        if 'Lonely Planet' not in block:
            # Find the last row of the Markdown table (starts with |)
            # We append our new row right after the last match of a table row
            new_block = re.sub(r'(\|\s*.*\|\n)(?!\|)', r'\1' + lp_row, block)
            content = content.replace(block, new_block)
            
    # Also handle the bulleted lists for hand-picked cities
    if '- **Activities**: [Viator Tours' in content and 'Lonely Planet' not in content:
        bullet = f"- **Guide**: [Lonely Planet {city_name}]({lp_clean_link})\n"
        content = re.sub(r'(-\s*\*\*Activities\*\*:.*\n)', r'\1' + bullet, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_re_add():
    count = 0
    total = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if 'cities' in root or 'cities' in dirs:
            target_dir = os.path.join(root, 'cities') if 'cities' in dirs else root
            for f in os.listdir(target_dir):
                if f.endswith('.md'):
                    total += 1
                    if re_add_lonely_planet(os.path.join(target_dir, f)):
                        count += 1
                        
    print(f"Re-added clean Lonely Planet links to {count} out of {total} city files.")

if __name__ == "__main__":
    run_re_add()
