import sys
from itertools import groupby

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 2)
    inv_fact[n + 1] = pow(fact[n + 1], MOD - 2, MOD)
    for i in range(n + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ids = {}  # canonical shape (sorted tuple of child ids) -> id
    ans = 1

    def multinomial_factor(children):
        # children: sorted list of child ids
        nonlocal ans
        k = len(children)
        f = fact[k]
        for _, grp in groupby(children):
            f = f * inv_fact[sum(1 for _ in grp)] % MOD
        ans = ans * f % MOD

    stack = [[]]  # stack of child-id lists; bottom is virtual root
    for c in s:
        if c == '(':
            stack.append([])
        else:
            children = stack.pop()
            children.sort()
            multinomial_factor(children)
            key = tuple(children)
            nid = ids.get(key)
            if nid is None:
                nid = len(ids)
                ids[key] = nid
            stack[-1].append(nid)
    root = stack[0]
    root.sort()
    multinomial_factor(root)
    print(ans % MOD)


main()
