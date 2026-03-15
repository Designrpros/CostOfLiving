import os
import re

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'
MARKER = '710853'

# Mapping of domain keywords to TP partner IDs
PARTNERS = {
    'booking.com': '121',
    'hotels.com': '285',
    'skyscanner': '100',  # Using Aviasales/Jetradar fallback or direct if supported
    'flixbus.com': '323',
    'raileurope.com': '276',
    'tripadvisor': '125',
    'airalo.com': '1890',
    'safetywing.com': '1470',
    'rentalcars.com': '136',
    'discovercars.com': '1630',
    'lonelyplanet.com': '170'
}

def monetize_link(url, partner_id):
    # Avoid double-wrapping
    if MARKER in url:
        return url
    
    # Standard TP Media redirect format
    # Using simple quoting for the URL to be safe in Markdown
    encoded_url = url.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
    return f"https://tp.media.r?marker={MARKER}&p={partner_id}&u={encoded_url}"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Regex to find markdown links: [label](url)
    # We look for the domains in our PARTNERS list
    for domain, pid in PARTNERS.items():
        # Match [label](https://domain...) where it's not already a tp.media link
        pattern = r'\[([^\]]+)\]\((https?://(?:www\.)?' + re.escape(domain) + r'[^\)]*)\)'
        
        def replacement(match):
            label = match.group(1)
            url = match.group(2)
            # Skip if already affiliate
            if 'tp.media' in url or MARKER in url or 'aid=' in url:
                 return match.group(0)
            
            monetized = monetize_link(url, pid)
            return f"[{label}]({monetized})"

        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_cleanup():
    count = 0
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.md'):
                if process_file(os.path.join(root, file)):
                    count += 1
    print(f"Done! Monetized links in {count} files.")

if __name__ == "__main__":
    run_cleanup()
