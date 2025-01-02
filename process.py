from PIL import Image
import numpy as np

class ImageLightpoint:
    def __init__(self, image_path: str, lightpoint: np.array(2,)):
        self.image_path = image_path
        self.lightpoint = lightpoint

def relight_image(image_path, color, image_num, resultant_array):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    modified_array = image_array * color
    modified_array = np.clip(modified_array, 0, 255).astype(np.uint8)
    modified_image = Image.fromarray(modified_array)
    modified_image.save(f"image{image_num}.png")
    resultant_array += modified_array

def mostLitArea(image_path: str) -> np.array(2,):
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
    pixel_norms = np.linalg.norm(image_array, axis=2) / 255
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            weight_x_index += pixel_norms[row, col] * np.array([row, col])
    #sum(weight)
    weight = 0
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            weight += pixel_norms[row, col]
    average_index = np.int64(np.floor(weight_x_index / weight))
    return average_index

def sortImages(images_and_lightpoints, num_of_col: int):
    # A simple selection sort algorithm to sort them with respect to their row index
    for i in range(len(images_and_lightpoints)):
        min: int = i
        for j in range(i+1, len(images_and_lightpoints)):
            if(images_and_lightpoints[j].lightpoint[0] < images_and_lightpoints[min].lightpoint[0]):
                min = j
        if i != min:
            temp = images_and_lightpoints[i]
            images_and_lightpoints[i] = images_and_lightpoints[min]
            images_and_lightpoints[min] = temp
    
    #after sorting slice the array and convert into a matrix
    sliced_list = [images_and_lightpoints[i:i+num_of_col] for i in range(0, len(images_and_lightpoints), num_of_col)]
    image_matrix = np.array(sliced_list)
    
    #now sort each row
    for i in range(image_matrix.shape[0]):
        for j in range(image_matrix.shape[1]):
            min: int = j
            for k in range(j+1, image_matrix.shape[1]):
                if(image_matrix[i, k].lightpoint[1] < image_matrix[i, min].lightpoint[1]):
                    min = k
            if j != min:
                tempo = image_matrix[i, j]
                image_matrix[i, j] = image_matrix[i, min]
                image_matrix[i, min] = tempo
    
    return image_matrix