#!/usr/bin/python
""" LZW encoder """
import sys


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


def fibonacci(number):
    pass


def encode(input_file, output_file, func=elias_omega):
    with open(input_file, "rb") as inp, open(output_file, "wb") as output:
        dictionary = []
        for i in range(256):
            dictionary.append(chr(i))

        bitstring_output = ""
        # get ascii char from byte
        P = chr(int.from_bytes(inp.read(1), 'big'))
        while True:
            tmp = inp.read(1)
            if len(tmp) == 0:
                break

            C = chr(int.from_bytes(tmp, 'big'))
            
            if P + C in dictionary:
                P = P + C
            else:
                bitstring_output += func(dictionary.index(P))
                dictionary.append(P + C)
                P = C
        bitstring_output += func(dictionary.index(P))
        if len(bitstring_output) % 8 != 0:
            bitstring_output += '0' * (8 - (len(bitstring_output) % 8))
        print(bitstring_output)
        b = bytes(
            int(bitstring_output[i : i + 8], 2)
            for i in range(0, len(bitstring_output), 8)
        )
        output.write(b)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        encode(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[3] == "--delta":
            encode(sys.argv[1], sys.argv[2], elias_delta) 
        if sys.argv[3] == "--gamma":
            encode(sys.argv[1], sys.argv[2], elias_gamma)
        if sys.argv[3] == "--omega":
            encode(sys.argv[1], sys.argv[2], elias_omega)
        if sys.argv[3] == "--fib":
            encode(sys.argv[1], sys.argv[2], fibonacci)
    else:
        print("encoder [input_file] [output_file] [coding_function, default=elias_omega]")
