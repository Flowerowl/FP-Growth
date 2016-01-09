# coding: utf-8
from collections import defaultdict
from itertools import imap

from .tree import Tree
from .node import Node


def find_support_items(transactions, min_support):
    items = defaultdict(lambda: 0)
    processed_transactions = []

    for trasaction in transactions:
        processed = []
        for item in trasaction:
            items[item] += 1
            processed.append(item)
        processed_transactions.append(processed)

    items = dict((item, support) for item, support in items.iteritems() if support >= min_support)

    return items


def clean_transaction(trasaction, items):
    trasaction = filter(lambda item: item in items, trasaction)
    trasaction.sort(key=lambda item: items[item], reverse=True)
    return trasaction


def find_with_suffix(tree, suffix, min_support):
    for item, nodes in tree.items():
        support = sum(n.count for n in nodes)
        if support >= min_support and item not in suffix:
            found_set = [item] + suffix
            yield (found_set, support)

            conditional_tree = conditional_tree_from_paths(tree.prefix_paths(item), min_support)
            for s in find_with_suffix(conditional_tree, found_set):
                yield s


def build_fptree(transactions):
    tree = Tree()
    for transaction in imap(clean_transaction, transactions):
        tree.add(transaction)

    return tree


def conditional_tree_from_paths(paths, min_support):
    tree = Tree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.find(node.item)
            if not next_point:
                item.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = Node(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    for item in items:
        support = sum(n.count for n in tree.nodes(item))
        if support < min_support:
            for node in tree.nodes(item):
                if node.parent is not None:
                    node.parent.remove(node)

    for node in tree.nodes(condition_item):
        if node.parent is not None:
            node.parent.remove(node)

    return tree
