#!/usr/bin/python
""" LZW encoder """
import sys
import math
from FibonacciCode import FibonacciCode


def elias_omega(number):
    code = "0"
    k = number
    while k > 1:
        binary_k = bin(k)[2:]
        code = binary_k + code
        k = len(binary_k) - 1
    return code


def elias_gamma(number):
    code = bin(number)[2:]
    code = "0" * (len(code) - 1) + code
    return code


def elias_delta(number):
    code = bin(number)[3:]
    code = elias_gamma(len(code) + 1) + code
    return code


def encode(input_file, output_file, func=elias_omega):
    with open(input_file, "rb") as inp, open(output_file, "wb") as output:
        dictionary = {}
        for i in range(256):
            dictionary[chr(i)] = i

        input_bytes = inp.read()

        bitstring_output = ""
        # get ascii char from byte
        P = chr(int.from_bytes([input_bytes[0]], "big"))
        for byte in input_bytes[1:]:
            C = chr(int.from_bytes([byte], "big"))

            if P + C in dictionary:
                P = P + C
            else:
                bitstring_output += func(dictionary[P] + 1)
                dictionary[P + C] = len(dictionary)
                P = C
        bitstring_output += func(dictionary[P] + 1)

        # padding thing
        if func.__name__ == "elias_gamma" or func.__name__ == "elias_delta":
            if len(bitstring_output) % 8 != 0:
                bitstring_output += "0" * (8 - (len(bitstring_output) % 8))
        else:
            if (len(bitstring_output) + 3) % 8 != 0:
                pad_len = (len(bitstring_output) + 3) % 8
                bitstring_output = bin(pad_len)[2:].zfill(3) + bitstring_output + "0" * pad_len
            else:
                bitstring_output = "000" + bitstring_output

        b = bytes(
            int(bitstring_output[i : i + 8], 2)
            for i in range(0, len(bitstring_output), 8)
        )
        output.write(b)
        return b


def entropy(freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i] / num_of_symbols * -math.log(freq[i] / num_of_symbols, 2)
    return H


def get_freq(sth):
    freq = {}

    for symbol in sth:
        if not symbol:
            break

        if symbol in freq:
            freq[symbol] += 1
        else:
            freq[symbol] = 1
    return freq


def stats(input_file, output):
    with open(input_file, "rb") as f:
        inp = f.read()
        input_len = len(inp)
        input_freq = get_freq(inp)

    output_len = len(output)
    output_freq = get_freq(output)

    print("Input entropy: ", entropy(input_freq, input_len))
    print("Output entropy: ", entropy(output_freq, output_len))
    print("Input size: ", input_len)
    print("Output size: ", output_len)
    print("Compression ratio: ", input_len / output_len)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        res = encode(sys.argv[1], sys.argv[2])
        stats(sys.argv[1], res)
    elif len(sys.argv) == 4:
        if sys.argv[3] == "--delta":
            res = encode(sys.argv[1], sys.argv[2], elias_delta)
        if sys.argv[3] == "--gamma":
            res = encode(sys.argv[1], sys.argv[2], elias_gamma)
        if sys.argv[3] == "--omega":
            res = encode(sys.argv[1], sys.argv[2], elias_omega)
        if sys.argv[3] == "--fib":
            res = encode(sys.argv[1], sys.argv[2], FibonacciCode().encode)

        stats(sys.argv[1], res)
    else:
        print(
            "encoder [input_file] [output_file] [coding_function, default=elias_omega]"
        )
