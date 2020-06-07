""" Program prównujący dwa pliki. Wypisuje ile 4-bitowych bloków jest różnych """

from sys import argv


def check(in1, in2):
    hex1 = in1.read().hex()
    hex2 = in2.read().hex()

    if len(hex1) != len(hex2):
        print("Pliki są różnej długości")
        return

    bits1 = "".join(
        [
            "{0:08b}".format(int(hex1[x : x + 2], base=16))
            for x in range(0, len(hex1), 2)
        ]
    )

    bits2 = "".join(
        [
            "{0:08b}".format(int(hex2[x : x + 2], base=16))
            for x in range(0, len(hex2), 2)
        ]
    )

    diffs = 0
    for i in range(0, len(bits1), 4):
        if bits1[i : i + 4] != bits2[i : i + 4]:
            diffs += 1

    if diffs == 0:
        print("Pliki są takie same")
    else:
        print(f"Pliki różnią się w {diffs} 4-bitowych blokach")


def main():
    if len(argv) == 3:
        in1 = argv[1]
        in2 = argv[2]

        with open(in1, "rb") as f1, open(in2, "rb") as f2:
            check(f1, f2)


if __name__ == "__main__":
    main()
