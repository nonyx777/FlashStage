from PIL import Image
import numpy as np

def process_image(image_path, color, image_num, resultant_array):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    modified_array = image_array * color
    modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
    modified_image = Image.fromarray(modified_array)
    modified_image.save(f"image{image_num}.png")
    resultant_array += modified_array