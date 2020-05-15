"""  Linde–Buzo–Gray (LGB) vector quantization """

from sys import argv
from math import floor, log
import lgb


def parse_bitmap(bitmap, width, height):
    result = []
    for i in range(width * height):
        # blue, green, red
        result.append((bitmap[i * 3], bitmap[i * 3 + 1], bitmap[i * 3 + 2]))
    return result


def quantify(bitmap, codebook):
    new_bitmap = []
    for pixel in bitmap:
        diffs = [lgb.euclid_squared(pixel, x) for x in codebook]
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


def mse(original, new):
    return (1 / len(original)) * sum(
        [lgb.euclid_squared(original[i], new[i]) ** 2 for i in range(len(original))]
    )


def power(x):
    return sum([i ** 2 for i in x])


def snr(x, mserr):
    return ((1 / len(x)) * sum([power(x[i]) for i in range(len(x))])) / mserr


def main():
    if len(argv) == 4:
        with open(argv[1], "rb") as f, open(argv[2], "wb") as output:
            tga = f.read()
            header = tga[:18]
            footer = tga[len(tga) - 26 :]
            width = tga[13] * 256 + tga[12]
            height = tga[15] * 256 + tga[14]
            original_bitmap = parse_bitmap(tga[18 : len(tga) - 26], width, height)

            codebook = lgb.generate_codebook(original_bitmap, 2 ** int(argv[3]))

            codebook = codebook_floor(codebook)
            new_bitmap = quantify(original_bitmap, codebook)
            payload = bitmap_to_bytes(new_bitmap)

            mserr = mse(original_bitmap, new_bitmap)
            snratio = snr(original_bitmap, mserr)

            print("MSE:", mserr)
            print("SNR:", snratio)

            new_tga = header + payload + footer
            output.write(new_tga)

    else:
        print("task1.py [input_file] [output_file] [2 ^ color_number]")


if __name__ == "__main__":
    main()
