import math
import sys

# Read N
N = int(input())

# Calculate minimum number of friends needed
M = math.ceil(math.log2(N)) if N > 1 else 1

# Print M
print(M)
sys.stdout.flush()

# Create distributions for each friend
# Friend i (0-indexed) gets bottles whose i-th bit is 1
distributions = [[] for _ in range(M)]

for bottle in range(1, N + 1):
    # Check each bit position for this bottle
    for friend_idx in range(M):
        # Check if bit friend_idx is set in bottle
        if (bottle >> friend_idx) & 1:
            distributions[friend_idx].append(bottle)

# Print the distributions
for bottles in distributions:
    output = [str(len(bottles))] + [str(b) for b in bottles]
    print(' '.join(output))
    sys.stdout.flush()

# Read the response
response = input().strip()

# Decode the bad bottle number from the response
bad_bottle = 0
for friend_idx in range(M):
    if response[friend_idx] == '1':
        bad_bottle |= (1 << friend_idx)

# Print the answer
print(bad_bottle)
sys.stdout.flush()
