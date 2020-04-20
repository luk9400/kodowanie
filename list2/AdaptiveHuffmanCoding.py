from Node import Node


class AdaptiveHuffmanCoding:
    def __init__(self):
        self.NYT = Node(symbol="NYT")
        self.root = self.NYT
        self.nodes = []
        self.visited = [None] * 256

    def swap(self, a, b):
        idx_a = self.nodes.index(a)
        idx_b = self.nodes.index(b)
        self.nodes[idx_a], self.nodes[idx_b] = self.nodes[idx_b], self.nodes[idx_a]

        a.parent, b.parent = b.parent, a.parent

        if a.parent.left is b:
            a.parent.left = a
        else:
            a.parent.right = a

        if b.parent.left is a:
            b.parent.left = b
        else:
            b.parent.right = b

    def get_largest_node(self, weight):
        for node in reversed(self.nodes):
            if node.weight == weight:
                return node

    def insert(self, s):
        node = self.visited[ord(s)]

        if node is None:
            spawn = Node(symbol=s, weight=1)
            internal = Node(self.NYT.parent, self.NYT, spawn, 1, "")
            spawn.parent = internal
            self.NYT.parent = internal

            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal

            self.nodes.insert(0, internal)
            self.nodes.insert(0, spawn)

            self.visited[ord(s)] = spawn
            node = internal.parent

        while node is not None:
            largest = self.get_largest_node(node.weight)

            if (
                node is not largest
                and node is not largest.parent
                and largest is not node.parent
            ):
                self.swap(node, largest)

            node.weight += 1
            node = node.parent

    def get_code(self, s, node, code=""):
        if node.left is None and node.right is None:
            if node.symbol == s:
                return code
            else:
                return ""
        else:
            tmp = ""
            if node.left is not None:
                tmp = self.get_code(s, node.left, code + "0")
            if not tmp and node.right is not None:
                tmp = self.get_code(s, node.right, code + "1")
            return tmp

    def encode(self, text):
        result = ""

        for s in text:
            if self.visited[ord(s)]:
                result += self.get_code(s, self.root)
            else:
                result += self.get_code("NYT", self.root)
                result += bin(ord(s))[2:].zfill(8)

            self.insert(s)

        return result

    def decode(self, text):
        symbol = chr(int(text[:8], base=2))
        result = symbol
        self.insert(symbol)
        node = self.root

        idx = 8
        while idx < len(text):
            if text[idx] == "0":
                node = node.left
            else:
                node = node.right

            symbol = node.symbol

            if symbol:
                if symbol == "NYT":
                    symbol = chr(int(text[idx + 1 : idx + 9], base=2))
                    idx += 8

                result += symbol
                self.insert(symbol)
                node = self.root

            idx += 1

        return result

    def write_to_file(self, text, filename):
        with open(filename, "wb") as f:
            if (len(text) + 3) % 8 != 0:
                pad_len = 8 - (len(text) + 3) % 8
                output = bin(pad_len)[2:].zfill(3) + text + "0" * pad_len
            else:
                output = "000" + text
            
            b = bytes(
                int(output[i:i + 8], base=2)
                for i in range(0, len(output), 8)
            )
            f.write(b)

    def read_from_file(self, filename):
        with open(filename, "rb") as f:
            hexstring = f.read().hex()
            bitstring = "".join(
                [
                    "{0:08b}".format(int(hexstring[x : x + 2], base=16))
                    for x in range(0, len(hexstring), 2)
                ]
            )

            num = bitstring[:3]
            bitstring = bitstring[3:len(bitstring)-int(num, base=2)]

            return bitstring
