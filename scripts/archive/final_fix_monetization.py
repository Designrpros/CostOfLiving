import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'
MARKER = '710853'

def fix_link(url):
    # Fix the typo tp.media.r -> tp.media/r
    new_url = url.replace('tp.media.r', 'tp.media/r')
    return new_url

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Fix the typo in all links
    content = content.replace('tp.media.r', 'tp.media/r')

    # 2. Standardize Booking.com table rows
    # Target: | [Booking.com](LINK) | Hotels |  -> | [Booking.com](LINK) | [Hotels](LINK) |
    booking_pattern = r'\| \[Booking\.com\]\((https?://tp\.media/r[^\)]+)\) \| Hotels \|'
    content = re.sub(booking_pattern, r'| [Booking.com](\1) | [Hotels](\1) |', content)

    # 3. Standardize TripAdvisor table rows
    # Target: | 📍 TripAdvisor | [Things to do...](LINK) | -> | [📍 TripAdvisor](LINK) | [Things to do...](LINK) |
    ta_pattern = r'\| 📍 TripAdvisor \| \[([^\]]+)\]\((https?://tp\.media/r[^\)]+)\) \|'
    content = re.sub(ta_pattern, r'| [📍 TripAdvisor](\2) | [\1](\2) |', content)

    # 4. Standardize Lonely Planet table rows
    lp_pattern = r'\| 📖 Lonely Planet \| \[([^\]]+)\]\((https?://tp\.media/r[^\)]+)\) \|'
    content = re.sub(lp_pattern, r'| [📖 Lonely Planet](\2) | [\1](\2) |', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_final_fix():
    count = 0
    total_files = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.md'):
                total_files += 1
                if process_file(os.path.join(root, f)):
                    count += 1
    print(f"Final fix complete. Standardized links in {count} out of {total_files} files.")

if __name__ == "__main__":
    run_final_fix()
