"""  Linde–Buzo–Gray (LGB) vector quantization """

from sys import argv
from math import floor
import py_lgb


def parse_bitmap(bitmap, width, height):
    result = []
    for i in range(width * height):
        # blue, green, red
        result.append((bitmap[i * 3], bitmap[i * 3 + 1], bitmap[i * 3 + 2]))
    return result


def quantify(bitmap, codebook):
    new_bitmap = []
    for pixel in bitmap:
        diffs = [py_lgb.euclid_squared(pixel, x) for x in codebook]
        new_bitmap.append(codebook[diffs.index(min(diffs))])
    return new_bitmap


def codebook_floor(codebook):
    new_codebook = []
    for color in codebook:
        new_codebook.append([floor(color[0]), floor(color[1]), floor(color[2])])
    return new_codebook


def bitmap_to_bytes(bitmap):
    payload = []
    for x in bitmap:
        for i in x:
            payload.append(i)
    return bytes(payload)


def main():
    if len(argv) == 4:
        with open(argv[1], "rb") as f, open(argv[2], "wb") as output:
            tga = f.read()
            header = tga[:18]
            footer = tga[len(tga) - 26 :]
            width = tga[13] * 256 + tga[12]
            height = tga[15] * 256 + tga[14]
            bitmap = parse_bitmap(tga[18 : len(tga) - 26], width, height)

            (
                codebook,
                codebook_abs_weights,
                codebook_rel_weights,
            ) = py_lgb.generate_codebook(bitmap, 2 ** int(argv[3]))

            codebook = codebook_floor(codebook)
            payload = bitmap_to_bytes(quantify(bitmap, codebook))

            new_tga = header + payload + footer
            output.write(new_tga)

    else:
        print("task1.py [input_file] [output_file] [2 ^ color_number (0-24)]")


if __name__ == "__main__":
    main()
