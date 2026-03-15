import shutil
import os

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'

def cleanup_praktisk():
    path = os.path.join(BASE_DIR, 'praktisk')
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Successfully removed legacy directory: {path}")
        except Exception as e:
            print(f"Error removing directory {path}: {e}")
    else:
        print(f"Directory {path} does not exist.")

if __name__ == "__main__":
    cleanup_praktisk()
