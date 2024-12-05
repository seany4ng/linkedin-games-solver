from collections import defaultdict

def reduce_sets(sets):
    # Step 1: Map colors to the sets they belong to
    color_to_sets = defaultdict(set)
    for set_index, s in enumerate(sets):
        for color in s:
            color_to_sets[color].add(set_index)

    # Debug: Print color_to_sets mapping
    print("Color to sets mapping:", dict(color_to_sets))

    # Step 2: Identify groups of `n` colors in `n` sets
    valid_groups = {}
    for color, indices in color_to_sets.items():
        indices = frozenset(indices)  # Ensure indices are hashable
        if len(indices) not in valid_groups:
            valid_groups[len(indices)] = defaultdict(set)
        valid_groups[len(indices)][indices].add(color)

    # Debug: Print valid groups
    print("Valid groups:", {k: dict(v) for k, v in valid_groups.items()})

    # Step 3: Reduce the sets based on valid groups
    for n, groups in valid_groups.items():
        for indices, colors in groups.items():
            if len(colors) == n:  # Only process if there are exactly `n` colors in `n` sets
                # Debug: Print reduction details
                print(f"Reducing sets {indices} to colors {colors}")
                for set_index in indices:
                    # Replace the set with the intersection of itself and the valid colors
                    sets[set_index] = sets[set_index].intersection(colors)
                    # Debug: Print the updated set
                    print(f"Updated set {set_index}: {sets[set_index]}")

    return sets

# Example usage
sets = [
    {0, 1, 2},
    {0, 1},
    {2}
]

reduced_sets = reduce_sets([set(s) for s in sets])
print("Final reduced sets:", [list(s) for s in reduced_sets])
