import pathlib
import os

num_skipped = 0
data_dir = pathlib.Path("data/").with_suffix("")
extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
for file in data_dir.rglob('*'):
    if file.suffix.lower() in extensions:
        try:
            fobj = open(file, "rb")
            is_jfif = b"JFIF" in fobj.peek(10)
        finally:
            fobj.close()

        if not is_jfif:
            num_skipped += 1
            # Delete corrupted image
            os.remove(file)

print(f"Deleted {num_skipped} images.")
