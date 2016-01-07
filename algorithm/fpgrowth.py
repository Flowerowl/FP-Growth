# coding: utf-8
from collections import defaultdict


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


def find_with_suffix(tree, suffix):
    pass


def find_frequent_items():
    pass


def conditional_tree_from_paths(paths, support):
    pass


def build_fptree():
    pass
