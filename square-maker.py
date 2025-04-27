from PIL import Image, ImageOps
import io
import glob
import os


def square_maker(file):
    """
    This will add padding to an image to make it square.
    Original file will be replaced!!
    """
    with Image.open(file) as image:
        real_size = image.size
        new_size = (max(real_size[0], real_size[1]), max(real_size[0], real_size[1]))

        image = ImageOps.pad(image, new_size, color="#000")

        new_filename = file + ".temp"
        image.save(new_filename, format="jpeg")
        os.remove(file)
        os.rename(new_filename, file)

files = glob.glob("./data/*/*")

for file in files:
    if file.count("/") > 3:
        print(file)
        raise ValueError("Dit kan niet. Er is meer nested folders dan verwacht.")

counter = 0
for file in files:
    square_maker(file)
    counter += 1
    print(f"I have edited {counter} files", end="\r")
