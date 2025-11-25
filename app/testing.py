colors = ["Red", "Black", "White"]
sizes = ["S", "M", "L"]
materials = ["Cotton", "Polyester"]

combinations = []

# Трехуровневая вложенность
for color in colors:
    for size in sizes:
        for material in materials:
            combinations.append((color, size, material))
print(combinations)
