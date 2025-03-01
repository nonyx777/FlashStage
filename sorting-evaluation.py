import numpy as np
import random

# Generate all images => Data to be acquired later
ROWS = 2
COLS = 3
all_images = []
for i in range(0, ROWS):
    for j in range(0, COLS):
        all_images.append([i, j])
        

# pick random indexes(images) from the list - no duplicates!
# This is what we are assuming when the user gives us incomplete data. I.e. we select a subset of the total images at random
IMAGES_PICKED = 6
total_images = ROWS * COLS
picked_images = random.sample(range(total_images), IMAGES_PICKED)

# Sort the picked images. eg [4, 2, 1] => [1, 2, 4]. 
# This gives us the true sort of the images
picked_images.sort()
true_sort_images = picked_images.copy()

# Now we put the same images in our previous sorting algortihm
# This step's result will be some permutation of the the picked_images.
# This is a blackbox implementation. The sorting algorithm we previously had needs to be a bit adapted to give us the output
random.shuffle(picked_images)

# compare each array index wise to get a rough and naive estimate of the error. 
error_sum = 0
for i in range(0, IMAGES_PICKED):
    if (true_sort_images[i] != picked_images[i]):
        error_sum += 1

print(error_sum / IMAGES_PICKED)

# We can use the manhatten distance for a more accurate description of the error
manhattenErrorSum = 0
for i in range(0, IMAGES_PICKED):
    true_image_index = all_images[true_sort_images[i]]
    processed_image_index = all_images[picked_images[i]]

    if ((true_image_index[0] != processed_image_index[0]) or (true_image_index[1] != processed_image_index[1])):
        manhattenErrorSum += abs(true_image_index[0] - processed_image_index[0]) + abs(true_image_index[1] - processed_image_index[1])      

print(manhattenErrorSum)

# Now, let's normalize the error by dividing with the maximum possible amount of manhatten error possible to get a value between 0 and 1
maximum_possible_manhattan_error_sum = 0
for i in range(ROWS):
    for j in range(COLS):
        max_distance = max(
            i + j,
            i + ((COLS - 1) - j),
            ((ROWS - 1) - i) + j,
            ((ROWS - 1) - i) + ((COLS - 1) - j)
        )
        maximum_possible_manhattan_error_sum += max_distance
        
normalized_manhatten_error = manhattenErrorSum / maximum_possible_manhattan_error_sum

print(normalized_manhatten_error)
