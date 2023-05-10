import os
from PIL import Image, ImageOps

# Set the input and output directories
input_dir = "./input"

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_trim_dir = "./output_trim"
if not os.path.exists(output_trim_dir):
    os.makedirs(output_trim_dir)

output_resized_dir = "./output_resized"
if not os.path.exists(output_resized_dir):
    os.makedirs(output_resized_dir)

def trim_png(filename):
    """Trims the empty space from a PNG file.
    Args:
        filename (str): The path to the input PNG file.
    Returns:
        The trimmed PIL image object.
    """
    # Open the image file and convert it to the RGBA mode
    with Image.open(filename).convert("RGBA") as img:
        # Convert the image to grayscale
        img_gray = img.convert("L")
        # Find the bounding box of the non-empty pixels in the image
        bbox = img_gray.getbbox()
        # Crop the image to the bounding box
        img_cropped = img.crop(bbox)
        # Return the trimmed image
        return img_cropped

def resize_image(img):
    """Resizes the input image to have a maximum width or height of 300 pixels while maintaining the aspect ratio.

    Args:
        img (PIL.Image): The input PIL image object.

    Returns:
        The resized PIL image object.
    """
    # Get the current size of the image
    width, height = img.size

    # Check if the image is already within the maximum size
    if width <= 300 and height <= 300:
        return img

    # Calculate the new size of the image while maintaining the aspect ratio
    if width > height:
        new_width = 300
        new_height = int(300 * height / width)
    else:
        new_height = 300
        new_width = int(300 * width / height)

    # Resize the image to the new size using bilinear interpolation
    img_resized = img.resize((new_width, new_height), resample=Image.BILINEAR)

    # Return the resized image
    return img_resized

def square_image(img_resized):
    """Fits the resized input image into a square of 300x300 pixels while maintaining the aspect ratio and filling the empty space with transparency.

    Args:
        img_resized (PIL.Image): The resized PIL image object.

    Returns:
        The squared PIL image object.
    """
    # Create a new RGBA image with transparent background
    img_square = Image.new("RGBA", (300, 300), (0, 0, 0, 0))

    # Calculate the coordinates to center the resized image in the new image
    x_offset = (300 - img_resized.width) // 2
    y_offset = (300 - img_resized.height) // 2

    # Paste the resized image onto the new image at the calculated coordinates
    img_square.paste(img_resized, (x_offset, y_offset))

    # Return the squared image
    return img_square

# Loop through each file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".png"):
        # Trim the PNG file and save the result to the output directory
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        trim_output_path = os.path.join(output_trim_dir, file_name)
        resi_output_path = os.path.join(output_resized_dir, file_name)
        # Trim image
        trimmed_img = trim_png(input_path)
        trimmed_img.save(trim_output_path, "PNG")
        # Resize image
        resized_image = resize_image(trimmed_img)
        resized_image.save(resi_output_path, "PNG")
        # Square
        out_image = square_image(resized_image)
        out_image.save(output_path, "PNG")