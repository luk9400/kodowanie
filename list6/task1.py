""" Filtry dolno i górnoprzepustowe """

from sys import argv


class EliasGamma:
    def encode(self, number):
        code = bin(number)[2:]
        code = "0" * (len(code) - 1) + code
        return code

    def decode(self, code):
        codes = []
        counter = 0
        idx = 0
        while idx < len(code):
            if code[idx] == "0":
                counter += 1
                idx += 1
            else:
                codes.append(int(code[idx : idx + counter + 1], base=2))
                idx += counter + 1
                counter = 0
        return codes


class Pixel:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        return Pixel(
            self.red + other.red, self.green + other.green, self.blue + other.blue
        )

    def __sub__(self, other):
        return Pixel(
            self.red - other.red, self.green - other.green, self.blue - other.blue
        )

    def __mul__(self, number):
        return Pixel(self.red * number, self.green * number, self.blue * number)

    def __div__(self, number):
        return Pixel(self.red / number, self.green / number, self.blue / number)

    def __floordiv__(self, number):
        return Pixel(self.red // number, self.green // number, self.blue // number)

    def __mod__(self, number):
        return Pixel(self.red % number, self.green % number, self.blue % number)

    def quantization(self, step):
        r = int(self.red // step * step)
        g = int(self.green // step * step)
        b = int(self.blue // step * step)
        return Pixel(r, g, b)


class Bitmap:
    def __init__(self, bitmap, width, height):
        self.width = width
        self.height = height

        result = []
        row = []
        for i in range(width * height):
            row.append(
                Pixel(
                    blue=bitmap[i * 3], green=bitmap[i * 3 + 1], red=bitmap[i * 3 + 2]
                )
            )

            if width == len(row):
                result.insert(0, row)
                row = []
        self.bitmap = result

    def __getitem__(self, pos):
        x, y = pos
        ret_x, ret_y = x, y
        if x < 0:
            ret_x = 0
        elif x >= self.width:
            ret_x = self.width - 1

        if y < 0:
            ret_y = 0
        elif y >= self.height:
            ret_y = self.height - 1

        return self.bitmap[ret_y][ret_x]


def parse_bitmap(bitmap, width, height):
    result = []
    row = []
    for i in range(width * height):
        row.append(
            Pixel(blue=bitmap[i * 3], green=bitmap[i * 3 + 1], red=bitmap[i * 3 + 2])
        )

        if width == len(row):
            result.insert(0, row)
            row = []
    return result


def filters(bitmap, x, y, high=False):
    weights_low = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    wegihts_high = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]

    weights = wegihts_high if high else weights_low

    pix = Pixel(0, 0, 0)
    for i in range(-1, 2):
        for j in range(-1, 2):
            pix += bitmap[x + i, y + j] * weights[i + 1][j + 1]

    weights_sum = sum([sum(row) for row in weights])

    if weights_sum <= 0:
        weights_sum = 1

    pix = pix // weights_sum

    pix.red = 0 if pix.red < 0 else pix.red
    pix.green = 0 if pix.green < 0 else pix.green
    pix.blue = 0 if pix.blue < 0 else pix.blue

    pix.red = 255 if pix.red > 255 else pix.red
    pix.green = 255 if pix.green > 255 else pix.green
    pix.blue = 255 if pix.blue > 255 else pix.blue

    return pix


def bitmap_to_array(bitmap):
    """ returns payload array for TGA file """
    payload = []
    for pixel in bitmap:
        payload += [pixel.blue, pixel.green, pixel.red]
    return payload


def bitmap_to_bytes(bitmap):
    payload = []
    for pixel in bitmap:
        payload += [pixel.blue, pixel.green, pixel.red]
    return bytes(payload)


def differential_coding(bitmap):
    a = bitmap[0]
    result = [a]
    for pixel in bitmap[1:]:
        a = pixel - a
        result.append(a)
        a = pixel

    return result


def differential_decoding(diffs):
    a = diffs[0]
    result = [a]
    for x in diffs[1:]:
        a = a + x
        result.append(a)
    return result


def quantify(bitmap, k):
    step = 256 // (2 ** k)
    return [pixel.quantization(step) for pixel in bitmap]


def encode(bitmap, k):
    filtered_low = [
        filters(bitmap, x, y)
        for y in reversed(range(bitmap.height))
        for x in range(bitmap.width)
    ]
    filtered_high = [
        filters(bitmap, x, y, True)
        for y in reversed(range(bitmap.height))
        for x in range(bitmap.width)
    ]

    byte_array = bitmap_to_array(filtered_low)
    byte_array = differential_coding(byte_array)

    # map all values to positive numbers for Elias coding
    # byte_array = [x + 256 for x in byte_array]
    byte_array = [2 * x if x > 0 else abs(x) * 2 + 1 for x in byte_array]

    bitstring = "".join([EliasGamma().encode(x) for x in byte_array])

    # pad bitstring with zeros
    if len(bitstring) % 8 != 0:
        bitstring += "0" * (8 - (len(bitstring) % 8))

    b = bytes(int(bitstring[i : i + 8], 2) for i in range(0, len(bitstring), 8))

    # now stuff for filtered_high
    quantified = quantify(filtered_high, k)
    quantified_bytes = bytes(bitmap_to_array(quantified))

    # tests stuff
    # flatten the bitmap
    bitmap = [
        bitmap[x, y]
        for y in reversed(range(bitmap.height))
        for x in range(bitmap.width)
    ]

    l_mse, l_mse_r, l_mse_g, l_mse_b, l_snr = tests(bitmap, filtered_low)
    h_mse, h_mse_r, h_mse_g, h_mse_b, h_snr = tests(bitmap, quantified)

    print("Low MSE:", l_mse)
    print("Low MSE (red):", l_mse_r)
    print("Low MSE (green):", l_mse_g)
    print("Low MSE (blue):", l_mse_b)
    print("Low SNR:", l_snr)
    print("High MSE:", h_mse)
    print("High MSE (red):", h_mse_r)
    print("High MSE (green):", h_mse_g)
    print("High MSE (blue):", h_mse_b)
    print("High SNR:", h_snr)

    return filtered_low, b, filtered_high, quantified_bytes


def decode(payload_low):
    hexstring = payload_low.hex()
    bitstring = "".join(
        [
            "{0:08b}".format(int(hexstring[x : x + 2], base=16))
            for x in range(0, len(hexstring), 2)
        ]
    )

    codes = EliasGamma().decode(bitstring)
    # diffs = [x - 256 for x in codes]
    diffs = [x // 2 if x % 2 == 0 else -(x // 2) for x in codes]

    bitmap = differential_decoding(diffs)

    return bytes(bitmap)


def d(a, b):
    return (a - b) ** 2


def mse(original, new):
    return (1 / len(original)) * sum([d(a, b) for a, b in zip(original, new)])


def snr(x, mserr):
    return ((1 / len(x)) * sum([d(i, 0) for i in x])) / mserr


def tests(original, new):
    original_array = []
    for pixel in original:
        original_array += [pixel.blue, pixel.green, pixel.red]

    original_red = [pixel.red for pixel in original]
    original_green = [pixel.green for pixel in original]
    original_blue = [pixel.blue for pixel in original]

    new_array = []
    for pixel in new:
        new_array += [pixel.blue, pixel.green, pixel.red]

    new_red = [pixel.red for pixel in new]
    new_green = [pixel.green for pixel in new]
    new_blue = [pixel.blue for pixel in new]

    mserr = mse(original_array, new_array)
    mserr_red = mse(original_red, new_red)
    mserr_green = mse(original_green, new_green)
    mserr_blue = mse(original_blue, new_blue)
    snratio = snr(original_array, mserr)
    return mserr, mserr_red, mserr_green, mserr_blue, snratio


def main():
    if len(argv) == 3:
        with open(argv[1], "rb") as f:
            tga = f.read()
            header = tga[:18]
            footer = tga[len(tga) - 26 :]
            width = tga[13] * 256 + tga[12]
            height = tga[15] * 256 + tga[14]

        if argv[2] == "--encode":
            bitmap = Bitmap(tga[18 : len(tga) - 26], width, height)

            if len(argv) == 4:
                k = argv[3]
            else:
                k = 2
            filtered_low, b, filtered_high, quantified = encode(bitmap, k)
            filtered_low = bytes(bitmap_to_array(filtered_low))
            filtered_high = bytes(bitmap_to_array(filtered_high))

            with open("output_low.tga", "wb") as f:
                f.write(header + filtered_low + footer)
            with open("output_low_encoded", "wb") as f:
                f.write(header + b + footer)
            with open("output_high.tga", "wb") as f:
                f.write(header + filtered_high + footer)
            with open("output_high_encoded.tga", "wb") as f:
                f.write(header + quantified + footer)

        if argv[2] == "--decode":
            payload = tga[18:-26]

            bitmap = decode(payload)

            with open("output_low_decoded.tga", "wb") as f:
                f.write(header + bitmap + footer)


if __name__ == "__main__":
    main()
