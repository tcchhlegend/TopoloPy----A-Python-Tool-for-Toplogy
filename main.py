from functools import reduce


def is_topological_space(X: set, R: list):
    if X not in R:
        return False
    if not set() in R:
        return False
    net = TopoNet(R)
    rt = net.root
    intersects = set()


def check_union_intersect(node, intersects):
    onto_children = [c.get_onto() for c in node.children]
    if len(onto_children):
        union = reduce(lambda x, y: x & y, onto_children)
        if (union not in onto_childen) or (union != node.get_onto()):
            return False
        n = len(onto_childen)
        indices = [(i, j) for i in range(n) for j in range(n) if i != j]
        for i, j in indices:
            intersects.add(onto_childen[i] | onto_childen[j])
if (intersects - net.net) != set():
    return False
return True


class Node:
    def __init__(self, onto):
        self.onto = onto
        self.parents = []
        self.children = []

    def is_child_of(self, parent):
        parent.children.append(self)
        self.parent.append(parent)

    def is_parent_of(self, child):
        child.parents.append(self)
        self.children.append(child)

    def has_offspring(self, other):
        level_set = self.children
        while len(level_set):
            if other in level_set:
                return True
            else:
                new_level_set = []
                for t in level_set:
                    new_level_set += t.children
                level_set = new_level_set
        return False

    def has_antecessor(self, other):
        level_set = self.parents
        while len(level_set):
            if other in level_set:
                return True
            else:
                new_level_set = []
                for t in level_set:
                    new_level_set += t.parents
                level_set = new_level_set
        return False

    def get_onto(self):
        return self.onto

    def __iter__(self):
        yield self
        for child in self.children:
            for child2 in iter(child):
                yield child2


class TopoNet:
    def __init__(self, R):
        self.net = set()
        self.leaves = set()
        self.root = None
        self._create_net(R)

    def _create_net(self, R):
        sorted_R = sorted(R, key=lambda x: len(x), reverse=True)
        node = Node(R[0])
        self.root = node
        self.net.add(node)
        self.leaves.add(node)
        for s in sorted_R[1:]:
            node = Node(s)
            level_set = list(self.leaves)
            flag = False
            for lf in level_set:
                if s.issubset(lf.get_onto()):
                    flag = True
                    node.is_child_of(lf)
                    break
                else:
                    level_set += lf.parents
            if not flag:
                return None
            self.leaves.add(node)
            self.leaves.remove(lf)
            self.net.add(node)


X = {1, 2, 3, 4}
R = [set(), {1, 2}, {3, 4}, {1, 5}, {1, 2, 3, 4}]
print(is_topological_space(X, R))
