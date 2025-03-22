import numpy as np
import argparse
import process
from PIL import Image
import os
import re

def get_images(paths):
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    image_files = []

    for path in paths:
        if os.path.isdir(path):
            # If it's a directory, get all images inside it
            image_files.extend(
                [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(supported_formats)]
            )
        elif os.path.isfile(path) and path.lower().endswith(supported_formats):
            # If it's an image file, add it directly
            image_files.append(path)
    
    return image_files

parser = argparse.ArgumentParser()
parser.add_argument("images", type=str, nargs='+', help="Paths to the images")
args = parser.parse_args()
image_paths = get_images(args.images)
images_and_lightpoints = []
col = 4


# images along with their lightpoints in a list
for image in image_paths:
    image_lightpoint = process.ImageLightpoint(image, process.mostLitArea(image))
    images_and_lightpoints.append(image_lightpoint)

image_matrix = process.sortImages(images_and_lightpoints, col)
index = 0
for row in range(image_matrix.shape[0]):
    for col in range(image_matrix.shape[1]):
        image = Image.open(image_matrix[row, col].image_path).convert("RGB")
        image_array = np.array(image)
        modified_array = image_array
        if image_matrix[row, col].lightpoint[0] != 0.0 and image_matrix[row, col].lightpoint[1] != 0.0:
            for i in range(image_matrix[row, col].lightpoint[0]-30, image_matrix[row, col].lightpoint[0]+30):
                for j in range(image_matrix[row, col].lightpoint[1]-30, image_matrix[row, col].lightpoint[1]+30):
                    modified_array[i, j] = np.array([255, 0, 0])
        modified_image = Image.fromarray(modified_array)
        #remove symbols from image path
        name = image_matrix[row, col].image_path
        pattern = r"[.|/]"
        name = [re.sub(pattern, '', s) for s in name]
        name = "".join(name)
        modified_image.save(f"./LitPoints/new_image{row}{col}_old_{name}.png")
        # print(f"{image_matrix[row, col].image_path} -> {image_matrix[row, col].lightpoint}")
        index += 1
