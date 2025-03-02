import numpy as np
from PIL import Image
import imageio
import argparse
import process
import os

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
col = 30
row = 18

### Sort Images
# images along with their lightpoints in a list
for image in image_paths:
    image_lightpoint = process.ImageLightpoint(image, process.mostLitArea(image))
    images_and_lightpoints.append(image_lightpoint)

sorted_image = process.sortImages(images_and_lightpoints, col)


### Reads the hdri array and divides it into specified grid
sky_array = imageio.imread("./HDRIs/street_lamp_4k.exr")
#convert to RGB if RGBA
if sky_array.shape[-1] == 4:
    sky_array = sky_array[..., :3]
else:
    sky_array = sky_array

sky_array = np.clip(sky_array, 0, None) ** (1/2.2)

print(f"Environment shape -> {sky_array.shape}")

num_of_row = int(sky_array.shape[0] / row)
num_of_col = int(sky_array.shape[1] / col)
print(f"Number of rows -> {num_of_row}")
print(f"Number of cols -> {num_of_col}")

sky_grid = [
    sky_array[i:i+num_of_row, j:j+num_of_col]
    for i in range(0, sky_array.shape[0], num_of_row)
    for j in range(0, sky_array.shape[1], num_of_col)
]


### Takes average of each divided patch (convert it into a single color)
### Multiply each path with their respective image
### While adding each result to the resultant array
# light using the environmental light
just_to_get_size = Image.open(image_paths[0]).convert("RGB")
size_array = np.array(just_to_get_size)
resultant_array = np.zeros_like(size_array).astype(np.float64)
sky_index = 0
for i in range(sorted_image.shape[0]):
    for j in range(sorted_image.shape[1]):
        image = Image.open(f"{sorted_image[i, j].image_path}").convert("RGB")
        image_array = np.array(image)
        average_color = np.average(sky_grid[sky_index], axis=(0, 1))
        modified_array = image_array * average_color
        modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
        modified_image = Image.fromarray(modified_array)
        modified_image.save(f"./LightedImages/image{sky_index}.png")
        # resultant_array += modified_array
        sky_index += 1

for i in range(len(image_paths)):
    image = Image.open(f"./LightedImages/image{i}.png").convert("RGB")
    image_array = np.array(image) / 255.0 
    image_array = np.clip(image_array, 0, 255).astype(np.float64)
    resultant_array += image_array

resultant_array = resultant_array / np.max(resultant_array) * 255
resultant_array = np.clip(resultant_array, 0, 255).astype(np.uint8)
final_image = Image.fromarray(resultant_array)
final_image.save("final.png")