import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'
MARKER = '710853'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Global typo fix (just in case)
    content = content.replace('tp.media.r', 'tp.media/r')

    # 2. Robust Booking.com Standardization
    # Matches: | [Booking.com](LINK) | Hotels | (with any whitespace)
    booking_pattern = r'\|\s*\[Booking\.com\]\((https?://tp\.media/r[^\)]+)\)\s*\|\s*Hotels\s*\|'
    content = re.sub(booking_pattern, r'| [Booking.com](\1) | [Hotels](\1) |', content)

    # 3. Robust TripAdvisor Standardization
    # Matches: | 📍 TripAdvisor | [Things to do...](LINK) | (with any whitespace)
    ta_pattern = r'\|\s*📍\s*TripAdvisor\s*\|\s*\[([^\]]+)\]\((https?://tp\.media/r[^\)]+)\)\s*\|'
    content = re.sub(ta_pattern, r'| [📍 TripAdvisor](\2) | [\1](\2) |', content)

    # 4. Robust Lonely Planet Standardization
    # Matches: | 📖 Lonely Planet | [Volos Guide](LINK) | (with any whitespace)
    lp_pattern = r'\|\s*📖\s*Lonely\s*Planet\s*\|\s*\[([^\]]+)\]\((https?://tp\.media/r[^\)]+)\)\s*\|'
    content = re.sub(lp_pattern, r'| [📖 Lonely Planet](\2) | [\1](\2) |', content)
    
    # 5. Handle rows that have NO link yet (e.g. for non-hub cities)
    # We need to find the city name from the H1
    h1_match = re.search(r'^#\s*(?:🏙️\s*)?([^ \n\r]+)', content, re.MULTILINE)
    if h1_match:
        city_name = h1_match.group(1).strip()
        
        # Booking.com injection if missing
        if '| Booking.com | Hotels |' in content or '| [Booking.com](https://www.booking.com' in content:
            bk_link = f"https://tp.media/r?marker={MARKER}&p=121&u=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Fss%3D{city_name}"
            content = content.replace('| [Booking.com](https://www.booking.com/searchresults.html?ss=' + city_name + ') | Hotels |', f'| [Booking.com]({bk_link}) | [Hotels]({bk_link}) |')
            content = content.replace('| Booking.com | Hotels |', f'| [Booking.com]({bk_link}) | [Hotels]({bk_link}) |')

        # TripAdvisor injection if missing
        ta_plain_pattern = r'\|\s*📍\s*TripAdvisor\s*\|\s*Things to do in\s+' + re.escape(city_name) + r'\s*\|'
        ta_link = f"https://tp.media/r?marker={MARKER}&p=125&u=https%3A%2F%2Fwww.tripadvisor.com%2FSearch%3Fq%3D{city_name}"
        content = re.sub(ta_plain_pattern, f'| [📍 TripAdvisor]({ta_link}) | [Things to do in {city_name}]({ta_link}) |', content)

        # Lonely Planet injection if missing
        lp_plain_pattern = r'\|\s*📖\s*Lonely\s*Planet\s*\|\s*'+re.escape(city_name)+r'\s+Guide\s*\|'
        lp_link = f"https://tp.media/r?marker={MARKER}&p=170&u=https%3A%2F%2Fwww.lonelyplanet.com%2Fsearch%3Fq%3D{city_name}"
        content = re.sub(lp_plain_pattern, f'| [📖 Lonely Planet]({lp_link}) | [{city_name} Guide]({lp_link}) |', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_deep_control():
    count = 0
    total_files = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.md'):
                total_files += 1
                if process_file(os.path.join(root, f)):
                    count += 1
    print(f"Control complete. Updated {count} out of {total_files} files.")

if __name__ == "__main__":
    run_deep_control()
