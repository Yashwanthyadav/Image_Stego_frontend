from PIL import Image

DELIMITER = "##STOP###"

def generate_data(pixels, data):
    data_bin = [format(ord(i), '08b') for i in data]
    image_data = iter(pixels)

    for binary_char in data_bin:
        pixels = list(
            next(image_data)[:3] +
            next(image_data)[:3] +
            next(image_data)[:3]
        )

        for i in range(8):
            if binary_char[i] == "1" and pixels[i] % 2 == 0:
                pixels[i] += 1
            elif binary_char[i] == "0" and pixels[i] % 2 != 0:
                pixels[i] -= 1

        if pixels[-1] % 2 != 0:
            pixels[-1] -= 1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

def encode_image(input_path, text, output_path):
    text += DELIMITER
    img = Image.open(input_path, "r")
    new_img = img.copy()

    size = img.size[0]
    x = y = 0

    for pixel in generate_data(img.getdata(), text):
        new_img.putpixel((x, y), pixel)
        if x == size - 1:
            x = 0
            y += 1
        else:
            x += 1

    new_img.save(output_path, "PNG")

def decode_image(input_path):
    img = Image.open(input_path, "r")
    image_data = iter(img.getdata())

    extracted = ""
    while True:
        pixels = list(
            next(image_data)[:3] +
            next(image_data)[:3] +
            next(image_data)[:3]
        )

        bin_str = "".join("0" if i % 2 == 0 else "1" for i in pixels[:8])
        char = chr(int(bin_str, 2))
        extracted += char

        if DELIMITER in extracted:
            return extracted.replace(DELIMITER, "")
