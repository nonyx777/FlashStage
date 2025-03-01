import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import argparse
import process
from PIL import Image
import numpy as np
import os

if not glfw.init():
    raise Exception("GLFW initialization failed!")

window = glfw.create_window(800, 600, "Editor", None, None)
if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window!")

glfw.make_context_current(window)

imgui.create_context()
renderer = GlfwRenderer(window)

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

def main():
    color1 = [0.5, 0.5, 0.5]
    color2 = [0.5, 0.5, 0.5]
    color3 = [0.5, 0.5, 0.5]

    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=str, nargs='+', help="Paths to the images")
    args = parser.parse_args()
    image_paths = get_images(args.images)

    #get the array of one of the images and zero it out
    final_array = np.zeros(np.array(Image.open(image_paths[0]).convert("RGB")).shape, dtype="uint8")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()

        imgui.new_frame()
        imgui.begin("Parameters", True)
        _, color1 = imgui.color_edit3("1st Image", *color1)
        _, color2 = imgui.color_edit3("2nd Image", *color2)
        _, color3 = imgui.color_edit3("3rd Image", *color3)

        colors = [color1, color2, color3]

        #IMAGE PROCESSING
        if imgui.button("Apply change"):
            final_array = np.zeros_like(final_array)
            for i in range(len(image_paths)):
                color = np.array(colors[i])
                process.relight_image(image_paths[i], color, i, final_array)
            final_image = Image.fromarray(final_array)
            final_image.save("final.png")

        imgui.end()

        imgui.render()
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    renderer.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()