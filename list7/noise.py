""" Program z prawdopodobieństwem p zamienia na przeciwny każdy bit z pliku in i zapisuje wynik w pliku out """

from random import random
from sys import argv


def swap(bit):
    return 1 if bit == "0" else 0


def make_some_noise(input_file, output_file, p):
    with open(input_file, "rb") as f, open(output_file, "wb") as out:
        payload = f.read()

        hexstring = payload.hex()
        bitstring = "".join(
            [
                "{0:08b}".format(int(hexstring[x : x + 2], base=16))
                for x in range(0, len(hexstring), 2)
            ]
        )

        new_bitstring = ""
        for bit in bitstring:
            if p > random():
                new_bitstring += str(swap(bit))
            else:
                new_bitstring += bit

        b = bytes(
            int(new_bitstring[i : i + 8], 2) for i in range(0, len(new_bitstring), 8)
        )
        out.write(b)


def main():
    if len(argv) == 4:
        p = float(argv[1])
        input_file = argv[2]
        output_file = argv[3]

        make_some_noise(input_file, output_file, p)


if __name__ == "__main__":
    main()
