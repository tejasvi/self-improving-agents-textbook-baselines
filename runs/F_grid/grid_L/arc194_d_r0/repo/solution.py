import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    MOD = 998244353

    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 2)
    inv_fact[n + 1] = pow(fact[n + 1], MOD - 2, MOD)
    for i in range(n + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # class id for each multiset of child class ids
    class_of_key = {}
    cnt = []  # cnt[class] = number of reachable strings for a node of this class

    def count_forest(child_ids):
        # number of distinct strings reachable from a forest whose
        # top-level items have the given class ids
        k = len(child_ids)
        res = fact[k]
        for c, m in Counter(child_ids).items():
            res = res * inv_fact[m] % MOD
            res = res * pow(cnt[c], m, MOD) % MOD
        return res

    def node_class(child_ids):
        key = tuple(sorted(child_ids))
        if key not in class_of_key:
            class_of_key[key] = len(cnt)
            cnt.append(count_forest(child_ids))
        return class_of_key[key]

    stack = [[]]  # each entry: list of child class ids
    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            stack[-1].append(node_class(children))

    top = stack[0]
    print(count_forest(top) % MOD)


main()
