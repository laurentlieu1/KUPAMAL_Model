import os
import sys
from PIL import Image

# Function to check if an image is fully black
def is_fully_black(image):
    grayscale_image = image.convert("L")
    histogram = grayscale_image.histogram()
    return histogram[0] == image.width * image.height


# Function to split and save parts of an image
def split_and_save(image_path, output_folder):
    # Open the image
    image = Image.open(image_path)
    # Calculate dimensions of each part
    width, height = image.size
    part_width = width // 2
    part_height = height // 2
    # Iterate over rows and columns to crop and save parts
    part_number = 1
    for row in range(2):
        for col in range(2):
            left = col * part_width
            top = row * part_height
            right = left + part_width
            bottom = top + part_height
            box = (left, top, right, bottom)
            part = image.crop(box)
            # Check if the part is fully black
            if not is_fully_black(part):
                part.save(
                    os.path.join(
                        output_folder,
                        f"{os.path.splitext(os.path.basename(image_path))[0]}_part_{part_number}.jpg",
                    )
                )
            part_number += 1


def process_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        # Create corresponding subfolders in the output directory
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        os.makedirs(output_subfolder, exist_ok=True)

        for filename in files:
            if (
                filename.endswith(".JPG")
                or filename.endswith(".jpeg")
                or filename.endswith(".png")
            ):
                image_path = os.path.join(root, filename)
                # Split and save parts of the image
                split_and_save(image_path, output_subfolder)


# Folder containing images
input_folder = os.getcwd() + "/input_folder/"
# Folder to save processed images
output_folder = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
try:
    process_folder(input_folder, output_folder)
    print("--------- SUCCES : Images rognées ---------")
    input("Appuyez sur Entrée pour quitter")
except Exception as error:
    print(f"--------- ERROR : {error} ---------")
    input("Appuyez sur Entrée pour quitter")
