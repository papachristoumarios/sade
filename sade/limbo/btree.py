import bisect
import copy
import limbo



class BTreeNode:

    def __init__(self, B, leaf):
        # Degree and leaf property
        self.B = B
        self.leaf = leaf

        # Keys and children
        self.keys = (2*B - 1)*[None]
        self.children = (2*B) * [None]

        # Number of keys
        self.n = 0

    def __repr__(self):
        return 'Keys: {} Children: {}'.format(str(self.keys), str(self.children))

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

            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            self.keys[i+1] = key;

            self.n += 1

        else:

            while i >= 0 and self.keys[i] > key:
                i -= 1

            if self.children[i + 1].n == 2 * self.B - 1:
                self.split_child(i + 1, self.children[i + 1])

                if self.keys[i + 1] < key:
                    i += 1

            self.children[i + 1].insert_non_full(key)

    def split_child(self, i, y):

        # Shallow copy
        z = copy.copy(y)
        z.n = self.B - 1

        for j in range(self.B - 1):
            z.keys[j] = y.keys[j + self.B]

        if not y.leaf:
            for j in range(self.B - 1):
                z.children[j] = y.children[j + self.B]
        y.n = self.B - 1

        for j in range(self.n, i, -1):
            self.children[j + 1] = self.children[j]

        self.children[i + 1] = z

        for j in range(self.n - 1, i - 1, -1):
            self.keys[j+1] = self.keys[j]

        self.keys[i] = y.keys[self.B-1];

        self.n += 1

    def collect_leaves(self, result):
        if self.leaf and self.n > 0:
            result.append(self)
            return result
        else:
            for i in range(self.n):
                self.children[i].collect_leaves(result)

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

    def __repr__(self):
        return self.root.__repr__()

    def insert(self, key):

        # Root is created
        if self.root == None:
            self.root = BTreeNode(self.B, True)
            self.root.keys[0] = key
            self.root.n = 1

        else:
            # The B-Tree is full so we need to change the root by splitting
            if self.root.n == 2 * self.B - 1:
                s = BTreeNode(self.B, False)
                s.children[0] = self.root

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

class DCFNode(BTreeNode):

    def __init__(self, B, leaf):
        super(DCFNode, self).__init__(B, leaf)
        self._merged = None
        self._dI = None

    @property
    def merged(self):
        if self.n == 1:
            self._dI = 0
            self.merged = self.keys[0]
        elif self.n > 1:
            temp_c, temp_dI = sade.limbo.Cluster.merge_clusters(self.keys[0], self.keys[1])
            for i in range(2, self.n):
                temp_c, temp_dI = sade.limbo.Cluster.merge_clusters(temp_c, self.keys[i])
            self._merged = temp_c
            self._dI = temp_dI

    def insert_non_full(self, key):

        i = self.n - 1

        argmin = 0
        minimum_dI = sys.maxsize

        for j in range(self.n):
            _, temp_dI = sade.limbo.Cluster.merge_clusters(self.keys[j], key)
            if temp_dI < minimum_dI:
                minimum_dI = temp_dI
                argmin = j

        if self.leaf:
            # Insert the key

            while i >= argmin:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            self.keys[i+1] = key;

            self.n += 1

        else:

            while i >= argmin: i -= 1

            if self.children[i + 1].n == 2 * self.B - 1:
                self.split_child(i + 1, self.children[i + 1])

                if self.keys[i + 1] < key:
                    i += 1

            self.children[i + 1].insert_non_full(key)

class DCFTree(BTree):

    def __init__(self, B, S):
        super(DCFTree, self).__init__(B)
        self.S = S
        self.leaves = None

    @property
    def border(self):
        if self.leaves == None:
            self.leaves = self.root.collect_leaves([])
        return self.leaves

    def cluster_leaves(self):
        self.cluster_leaves = [b.merged for b in self.border]
        return self.cluster_leaves
