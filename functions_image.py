from PIL import Image

def encode_greyscale_image_to_8bit(image):
    """
    Convert a greyscale image to 8bit binary ready for encoding into .wav format
    Iterate over pixels, convert each pixel's 0-255 value to 8bit binary

    :param image:   array       2-dimensional array of pixel luminosities
    :return:        list        image binary data
    """
    output = []

    # Iterate rows
    for i in range(image.height):
        # Iterate columns
        for j in range(image.width):
            # Get pixel value
            pixel = image.getpixel((j, i))

            # Convert to 8bit binary
            pixel_bin = bin(pixel)[2:].zfill(8)

            # Append to output list
            output += [int(x) for x in pixel_bin]

            # print(pixel)
            # print(pixel_bin)

    return output

