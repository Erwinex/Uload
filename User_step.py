from collections import defaultdict


def tree():
    return defaultdict(tree)


user_step = tree()
