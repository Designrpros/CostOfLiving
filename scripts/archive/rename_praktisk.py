import os

BASE_DIR = '/home/vegar/.openclaw/workspace/costofliving/europa/docs'

def rename_praktisk():
    old_path = os.path.join(BASE_DIR, 'praktisk')
    new_path = os.path.join(BASE_DIR, 'practical')
    
    if os.path.exists(old_path):
        if os.path.exists(new_path):
            print("Error: Destination 'practical' already exists.")
        else:
            os.rename(old_path, new_path)
            print(f"Successfully renamed {old_path} to {new_path}")
    else:
        print(f"Error: Source {old_path} does not exist.")

if __name__ == "__main__":
    rename_praktisk()
