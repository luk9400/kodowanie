from sys import argv

G = [
    "00000000",
    "11010010",
    "01010101",
    "10000111",
    "10011001",
    "01001011",
    "11001100",
    "00011110",
    "11100001",
    "00110011",
    "10110100",
    "01100110",
    "01111000",
    "10101010",
    "00101101",
    "11111111",
]

errors = 0


def from_hamming(bits):
    for code in G:
        hamm1 = [int(k) for k in bits]
        hamm2 = [int(k) for k in code]

        diff = []

        i = 0
        while i < 8:
            if hamm1[i] != hamm2[i]:
                diff.append(i + 1)
            i += 1

        if len(diff) == 0:
            return bits[2] + bits[4] + bits[5] + bits[6]

        if len(diff) == 1:
            return code[2] + code[4] + code[5] + code[6]

        if len(diff) == 2:
            global errors
            errors += 1
            return None

    return None


def decode(bitstring):
    decoded = ""

    while len(bitstring) >= 8:
        nibble = bitstring[0:8]
        nibble = from_hamming(nibble)

        if nibble != None:
            decoded += nibble
        else:
            decoded += "0000"

        bitstring = bitstring[8:]

    print(f"W {errors} blokach napotkano 2 błędy")

    return decoded


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

            result = decode(bitstring)
            b = bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))

            output.write(b)


if __name__ == "__main__":
    main()
