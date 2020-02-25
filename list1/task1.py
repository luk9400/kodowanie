import math

def func(filename):
    with open(filename, 'r') as f:
        symbols_frequency = {}
        num_of_symbols = 0
        while True:
            symbol = f.read(1)
            if not symbol:
                break

            num_of_symbols += 1

            if symbol in symbols_frequency:
                symbols_frequency[symbol] += 1
            else:
                symbols_frequency[symbol] = 1
        print(symbols_frequency)
        print(entropy(symbols_frequency, num_of_symbols))

def entropy(freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i]/num_of_symbols * -math.log(freq[i]/num_of_symbols, 2)
    return H

func('pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt')