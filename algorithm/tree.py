# coding: utf-8
from collections import namedtuple

from .node import Node


class Tree(object):
    Route = namedtuple('Route', 'head tail')

    def __init__(self):
        self._root = Node(self, None, None)
        self._routes = {}

    @property
    def root(self):
        return self._root

    def add(self, transaction):
        point = self._root

        for item in transaction:
            next_point = point.find(item)
            if next_point:
                next_point.increment()
            else:
                next_point = Node(self, item)
                point.add(next_point)
                self._update_route(next_point)

            point = next_point

    def _update_route(self, point):
        try:
            route = self._routes[point.item]
            route[1].neighbor = point
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        for item in self._routes.iterkeys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        try:
            node = self._routes[item][0]
        except:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        def collect_path(node):
            path = []
            while node and not node.is_root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

    def inspect(self):
        print 'Tree:'
        self.root.inspect(1)
        print
        print 'Routes:'
        for item, nodes in self.items():
            print '  %r' % item
            for node in nodes:
                print '   %r' % node

    def _removed(self, node):
        head, tail = self._routes[node.item]
        if node is head:
            if node is tail or not node.neighbor:
                del self._routes[node.item]
            else:
                self._routes[node.item] = self.Route(node.neighbor, tail)
        else:
            for n in self.nodes(node.item):
                if n.neighbor is node:
                    n.neighbor = node.neighbor
                    if node is tail:
                        self._routes[node.item] = self.Route(head, n)
                    break
