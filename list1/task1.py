import math
import sys


def func(filename):
    with open(filename, 'rb') as f:
        symbols_frequency = {}
        cond_freq = {}
        num_of_symbols = 0
        prev_symbol = b'\x00'
        cond_freq[prev_symbol] = {}

        while True:
            symbol = f.read(1)
            if not symbol:
                break

            num_of_symbols += 1

            if prev_symbol not in cond_freq:
                cond_freq[prev_symbol] = {}

            if symbol in cond_freq[prev_symbol]:
                cond_freq[prev_symbol][symbol] += 1
            else:
                cond_freq[prev_symbol][symbol] = 1

            prev_symbol = symbol

            if symbol in symbols_frequency:
                symbols_frequency[symbol] += 1
            else:
                symbols_frequency[symbol] = 1

        # print(symbols_frequency)
        # print(cond_freq)
        print(entropy(symbols_frequency, num_of_symbols))
        print(cond_entropy(cond_freq, symbols_frequency, num_of_symbols))


def entropy(freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i]/num_of_symbols * -math.log(freq[i]/num_of_symbols, 2)
    return H


def cond_entropy(cond_freq, freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i]/num_of_symbols * sum(cond_freq[i][j]/freq[i] * -math.log(
            cond_freq[i][j]/freq[i], 2) for j in cond_freq[i])
    return H


if __name__ == '__main__':
    filename = sys.argv[1]
    func(filename)
