import math
import sys

def func(filename):
    with open(filename, 'rb') as f:
        symbols_frequency = {}
        b = {}
        num_of_symbols = 0
        prev_symbol = chr(0)
        b[prev_symbol] = {}

        while True:
            symbol = f.read(1)
            if not symbol:
                break

            num_of_symbols += 1

            if prev_symbol not in b:
                b[prev_symbol] = {}

            if symbol in b[prev_symbol]:
                b[prev_symbol][symbol] += 1
            else:
                b[prev_symbol][symbol] = 1

            prev_symbol = symbol

            if symbol in symbols_frequency:
                symbols_frequency[symbol] += 1
            else:
                symbols_frequency[symbol] = 1
            
        print(symbols_frequency)
        print(b)
        print(entropy(symbols_frequency, num_of_symbols))

def entropy(freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i]/num_of_symbols * -math.log(freq[i]/num_of_symbols, 2)
    return H

def cond_entropy(cond_freq, freq):
    pass

if __name__ == '__main__':
    filename = sys.argv[1]
    func(filename)