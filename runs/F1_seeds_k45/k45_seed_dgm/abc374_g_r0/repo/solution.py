from collections import defaultdict

n = int(input())
products = []
for _ in range(n):
    products.append(input().strip())

# Build the graph
in_degree = defaultdict(int)
out_degree = defaultdict(int)

for product in products:
    from_letter = product[0]
    to_letter = product[1]
    out_degree[from_letter] += 1
    in_degree[to_letter] += 1

# Get all letters that appear
all_letters = set()
for product in products:
    all_letters.add(product[0])
    all_letters.add(product[1])

# Count vertices where out-degree > in-degree
sources = 0
for letter in all_letters:
    if out_degree[letter] > in_degree[letter]:
        sources += 1

# The answer is the number of vertices with out-degree > in-degree
# Or equivalently, the number of vertices with in-degree > out-degree
# They should be equal by graph theory
print(sources if sources > 0 else 1)
