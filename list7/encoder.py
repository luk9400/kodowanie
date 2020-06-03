""" Encodes file with Hamming(8, 4) code """

from sys import argv


def parity(bitstring, indices):
    sub = ""

    for i in indices:
        sub += bitstring[i]

    return str(str.count(sub, "1") % 2)


def to_hamming(bits):
    p1 = parity(bits, [0, 1, 3])
    p2 = parity(bits, [0, 2, 3])
    p3 = parity(bits, [1, 2, 3])
    p = parity(p1 + p2 + bits[0] + p3 + bits[1:], range(7))

    return p1 + p2 + bits[0] + p3 + bits[1:] + p


def encode(bitstring):
    encoded = ""

    while len(bitstring) >= 4:
        nibble = bitstring[0:4]
        encoded += to_hamming(nibble)
        bitstring = bitstring[4:]

    return encoded


def main():
    if len(argv) == 3:
        with open(argv[1], "rb") as f, open(argv[2], "wb") as output:
            payload = f.read()

            hexstring = payload.hex()
            bitstring = "".join(
                [
                    "{0:08b}".format(int(hexstring[x : x + 2], base=16))
                    for x in range(0, len(hexstring), 2)
                ]
            )

            result = encode(bitstring)
            b = bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))

            output.write(b)


if __name__ == "__main__":
    main()
