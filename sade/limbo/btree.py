import bisect
import copy

class BTreeNode:

    def __init__(self, B, leaf):
        # Degree and leaf property
        self.B = B
        self.leaf = leaf

        # Keys and children
        self.keys = []
        self.children = []

        # Number of keys
        self.n = 0

    def traverse(self):
        if not self.leaf:
            for i in range(self.n):
                self.children[i].traverse()

    def search(self, key):
        i = 0

        while i < self.n and key > keys[i]:
            i += 1

        if keys[i] == key:
            return self

        if self.leaf:
            return None

        return self.children[i].search(key)

    def insert_non_full(self, key):

        i = self.n - 1

        if self.leaf:
            # Insert the key
            bisect.insort(self.keys, key)

            self.n += 1

        else:

            while i >= 0 and self.keys[i] > key:
                i -= 1

            if self.children[i + 1].n == 2 * self.B - 1:
                self.split_child(i + 1, self.children[i + 1])

                if keys[i + 1] < self.k:
                    i += 1

            self.children[i + 1].insert_non_full(key)

    def split_child(self, y):
        # TODO Finish

        # Shallow copy
        z = copy.copy(y)
        z.n = self.B - 1

        z.keys = z.keys[-z.n:]



    class BTree:

        def __init__(self, B):
            self.B = B
            self.root = None

        def traverse(self):
            if self.root != None:
                self.root.traverse()

        def search(self, key):
            if self.root != None:
                self.root.search(key)

        def insert(self, key):

            # Root is created
            if self.root == None:
                self.root = BTreeNode(self.B)
                self.root.keys.append(key)
                self.root.n = 1

            else:
                # The B-Tree is full so we need to change the root by splitting
                if self.root.n == 2 * self.B - 1:
                    s = BTreeNode(self.B, False)
                    s.children.append(self.root)

                    # Split and insert
                    s.split_child(0, self.root)

                    i = 0
                    if s.keys[0] < key:
                        i += 1

                    s.children[i].insert_non_full(key)

                    # Change root
                    self.root = s

                else:

                    self.root.insert_non_full(key)
