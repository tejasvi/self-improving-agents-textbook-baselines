def is_subsequence(s, t):
    """Check if t is a subsequence of s"""
    t_idx = 0
    for char in s:
        if t_idx < len(t) and char == t[t_idx]:
            t_idx += 1
    return t_idx == len(t)

# Read input
n, target = input().split()
n = int(n)
strings = []
for _ in range(n):
    strings.append(input().strip())

# Count pairs
count = 0
for i in range(n):
    for j in range(n):
        concatenated = strings[i] + strings[j]
        if is_subsequence(concatenated, target):
            count += 1

print(count)
