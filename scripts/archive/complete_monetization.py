import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'
MARKER = '710853'

def wrap_link(url, p_id):
    # Avoid double wrapping
    if 'tp.media' in url or MARKER in url:
        return url
    encoded_url = url.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
    return f"https://tp.media/r?marker={MARKER}&p={p_id}&u={encoded_url}"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # TripAdvisor (P=125)
    ta_pattern = r'\[([^\]]+)\]\((https?://(?:www\.)?tripadvisor\.[a-z\./]+[^\)]*)\)'
    content = re.sub(ta_pattern, lambda m: f"[{m.group(1)}]({wrap_link(m.group(2), '125')})", content, flags=re.IGNORECASE)

    # Lonely Planet (P=170)
    lp_pattern = r'\[([^\]]+)\]\((https?://(?:www\.)?lonelyplanet\.[a-z\./]+[^\)]*)\)'
    content = re.sub(lp_pattern, lambda m: f"[{m.group(1)}]({wrap_link(m.group(2), '170')})", content, flags=re.IGNORECASE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_sweep():
    count = 0
    total_files = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if 'cities' in dirs or 'byer' in dirs: # Handle both naming conventions just in case
            target_dir = os.path.join(root, 'cities') if 'cities' in dirs else os.path.join(root, 'byer')
            for f in os.listdir(target_dir):
                if f.endswith('.md'):
                    total_files += 1
                    if process_file(os.path.join(target_dir, f)):
                        count += 1
    print(f"Sweep complete. Monetized links in {count} out of {total_files} city files.")

if __name__ == "__main__":
    run_sweep()
