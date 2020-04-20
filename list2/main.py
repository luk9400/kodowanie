from AdaptiveHuffmanCoding import AdaptiveHuffmanCoding
import sys
import math


def entropy(string):
    freq = {}

    for char in string:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    H = 0
    for i in freq:
        H += freq[i] / len(string) * -math.log(freq[i] / len(string), 2)

    return H


def main(args):
    if len(args) == 4:
        if args[3] == "--decode":
            text = AdaptiveHuffmanCoding().read_from_file(args[1])
            result = AdaptiveHuffmanCoding().decode(text)

            with open(args[2], "w") as output:
                output.write(result)

        elif args[3] == "--encode":
            with open(args[1]) as inp:
                text = inp.read()

            result = AdaptiveHuffmanCoding().encode(text)
            print("Entropy: ", entropy(text))
            print("Average length: ", len(result) / len(text))
            print("Compression ratio: ", len(text) * 8 / len(result))

            AdaptiveHuffmanCoding().write_to_file(result, args[2])

    else:
        print("main [input_file] [output_file] [--encode/--decode]")


if __name__ == "__main__":
    main(sys.argv)
