import os
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
                part.save(os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}_part_{part_number}.jpg"))
            part_number += 1

# Folder containing images
input_folder = os.getcwd() + "/input_folder/"
# Folder to save processed images
output_folder = "output"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
try : 
# Iterate through all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".JPG") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            # Split and save parts of the image
            split_and_save(image_path, output_folder)

    print("--------- SUCCES : Images rognées ---------")

except Exception as error :
    print(f"--------- ERROR : {error} ---------")
