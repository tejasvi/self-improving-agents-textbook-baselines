import sys
import math

# Read N
N = int(input())

# Calculate minimum number of friends needed
# We need M bits to represent N different bottles
# 2^M >= N, so M >= log2(N)
M = (N - 1).bit_length()  # This gives ceil(log2(N)) for N >= 1

# Print M
print(M)
sys.stdout.flush()

# Distribute juice to friends using binary encoding
# Friend i (0-indexed) gets all bottles where bit i is set in the bottle number
friends_bottles = [[] for _ in range(M)]

for bottle in range(1, N + 1):
    # Get binary representation of bottle number
    for bit_idx in range(M):
        # Check if bit_idx-th bit is set in bottle
        if (bottle >> bit_idx) & 1:
            friends_bottles[bit_idx].append(bottle)

# Print the distribution
for i in range(M):
    bottles = friends_bottles[i]
    print(len(bottles), *bottles)
sys.stdout.flush()

# Read results
result_string = input().strip()

# Decode the result
# The result_string tells us which friends got sick
# Friend i got sick if result_string[i] == '1'
# This directly gives us the binary representation of the spoiled bottle

spoiled_bottle = 0
for i in range(M):
    if result_string[i] == '1':
        spoiled_bottle |= (1 << i)

# Print the answer
print(spoiled_bottle)
sys.stdout.flush()
