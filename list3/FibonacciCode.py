class FibonacciCode:
    def fib_sequence(self, n, decode=False):
        l = []
        a = 0
        b = 1

        if decode:
            for _ in range(n + 2):
                l.append(a)
                a, b = b, a + b
        else:
            while a <= n:
                l.append(a)
                a, b = b, a + b
        return l[2:]            

    def encode(self, n):
        seq = self.fib_sequence(n)
        res = ["0" for _ in seq]

        while n > 0:
            i, x = [(i, x) for i, x in enumerate(seq) if x <= n][-1]
            res[i] = "1"
            n %= x
        res.append("1")
        return "".join(res)

    def decode(self, code):
        codes = [x + "1" for x in code.split("11")][0:-1]
        seq = self.fib_sequence(max([len(x) for x in codes]), True)
        return [
            sum([seq[i] if x == "1" else 0 for i, x in enumerate(code)])
            for code in codes
        ]
