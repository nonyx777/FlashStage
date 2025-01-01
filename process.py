from PIL import Image
import numpy as np

def relight_image(image_path, color, image_num, resultant_array):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    modified_array = image_array * color
    modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
    modified_image = Image.fromarray(modified_array)
    modified_image.save(f"image{image_num}.png")
    resultant_array += modified_array

def most_lit_area(image_path: str):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    treshold: float = 1.0
    #calculate magnitude of each color in the matrix
    pixel_norms = np.linalg.norm(image_array, axis=2) / 255
    bright_mask = pixel_norms < treshold
    #only colors with magnitude above the specified
    #treshold are left
    image_array[bright_mask] = np.array([0, 0, 0])
    #sum(weight * index), where weight is the color magnitude
    #and index as the pixel location
    weight_x_index = np.zeros((2, ))
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            weight_x_index += pixel_norms[row, col] * np.array([row, col])
    #sum(weight)
    weight = 0
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            weight += pixel_norms[row, col]
    average_index = np.int64(np.floor(result1 / result2))
    return average_index

