# coding: utf-8


class Node(object):

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    @property
    def tree(self):
        return self._tree

    @property
    def item(self):
        return self._item

    @property
    def count(self):
        return self._count

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if isinstance(value, Node):
            self._parent = value

    @property
    def neighbor(self):
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if isinstance(value, Node):
            self._neighbor = value

    @property
    def children(self):
        return tuple(self._children.itervalues())

    @property
    def increment(self):
        self._count += 1

    @property
    def is_root(self):
        return self._item is None and self._count is None

    @property
    def is_leaf(self):
        return len(self._children) == 0

    def add(self, child):
        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def find(self, item):
        try:
            return self._children[item]
        except KeyError:
            return None

    def remove(self, child):
        del self._children[child.item]
        child.parent = None
        self._tree._removed(child)

        for sub_child in child.children:
            try:
                self._children[sub_child.item]._count += sub_child.count
            except KeyError:
                self.add(sub_child)
        child._children = {}

    def inspect(self, depth=0):
        print ('  ' * depth + repr(self))
        for child in self.children:
            child.inspect(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r, (%r)>" % (type(self).__name__, self.item, self.count)

    def __contains__(self, item):
        return item in self._children

