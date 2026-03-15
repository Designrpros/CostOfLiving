import os
import shutil

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'

def finalize_naming():
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if 'byer' in dirs:
            old_path = os.path.join(root, 'byer')
            new_path = os.path.join(root, 'cities')
            
            # If cities already exists, merge them
            if os.path.exists(new_path):
                print(f"Merging {old_path} into {new_path}...")
                for item in os.listdir(old_path):
                    s = os.path.join(old_path, item)
                    d = os.path.join(new_path, item)
                    if os.path.isfile(s):
                        shutil.move(s, d)
                os.rmdir(old_path)
            else:
                print(f"Renaming {old_path} -> {new_path}")
                os.rename(old_path, new_path)
            count += 1
    
    print(f"Done! Fixed {count} folders.")

if __name__ == "__main__":
    finalize_naming()
