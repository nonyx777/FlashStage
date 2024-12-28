from PIL import Image
import numpy as np
import argparse

WHITE = np.ones(3,)
RED = np.array([1, 0, 0])
GREEN = np.array([0, 1, 0])
BLUE = np.array([0, 0, 1])

def process_image(image_path, COLOR, image_num, resultant_array):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    modified_array = image_array * COLOR
    modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
    modified_image = Image.fromarray(modified_array)
    modified_image.save(f"image{image_num}.png")
    resultant_array += modified_array

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=str, nargs='+', help="Paths to the images")

    args = parser.parse_args()

    #get the array of one of the images and zero it out
    final_array = np.zeros(np.array(Image.open(args.images[0]).convert("RGB")).shape, dtype=np.uint8)
    index = 0
    for image_path in args.images:
        color = RED if index == 0 else GREEN if index == 1 else BLUE
        process_image(image_path, color, index, final_array)
        index+=1
    final_image = Image.fromarray(final_array)
    final_image.save("final.png")

if __name__ == "__main__":
    main()