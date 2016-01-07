# coding: utf-8


class Node(object):

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

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
        pass

    def __contains__(self, item):
        return item in self._children

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
    def increment(self):
        self._count += 1

    @property
    def is_root(self):
        return self._item is None and self._count is None

    @property
    def is_leaf(self):
        return len(self._children) == 0

    @property
    def children(self):
        return tuple(self._children.itervalues())
