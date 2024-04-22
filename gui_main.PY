import tkinter as tk
import copy

def forward_checking(assignment, domains, regions):
    if len(assignment) == len(regions):
        return assignment
    var = mrv(assignment, domains)
    for value in lcv(var, assignment, domains, regions):
        new_assignment = copy.deepcopy(assignment)
        new_domains = copy.deepcopy(domains)
        new_assignment[var] = value
        new_domains[var] = [value]
        for neighbor in regions[var]:
            if neighbor not in new_assignment:
                if value in new_domains[neighbor]:
                    new_domains[neighbor].remove(value)
                    if not new_domains[neighbor]:
                        continue
        result = forward_checking(new_assignment, new_domains, regions)
        if result is not None:
            return result
    return None

def mrv(assignment, domains):
    unassigned_vars = [var for var in domains if var not in assignment]
    if not unassigned_vars:
        return None
    return min(unassigned_vars, key=lambda var: len(domains[var]))

def lcv(var, assignment, domains, regions):
    values = domains[var]
    counts = []
    for value in values:
        count = 0
        for neighbor in regions[var]:
            if neighbor not in assignment:
                if value in domains[neighbor]:
                    count += 1
        counts.append(count)
    return [value for _, value in sorted(zip(counts, values))]

def degree(var, assignment, regions):
    return len(regions[var])

def color_map():
    global assignment, colors, regions, grid
    result = forward_checking(assignment, domains, regions)
    if result is None:
        print('No solution found.')
    else:
        print(result)
        for i, region in enumerate(regions):
            for j in range(5):
                grid[i][j] = result[region]
        draw_grid()

def draw_grid():
    canvas.delete("all")
    color_map = {color.strip(): i for i, color in enumerate(colors)}
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x1, y1 = j * 50, i * 50
            x2, y2 = (j + 1) * 50, (i + 1) * 50
            if cell!= '0':
                color = colors[int(cell) - 1].strip()
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white')

# Initialize the data structures
regions = {}
while True:
    key = input("Enter a key (press Enter to stop): ")
    if not key:
        break
    l1=[]
    while True:
        value = input("Enter the value for the key '{}': ".format(key))
        if not value:
            regions[key] = l1
            break
        l1.append(value)
        regions[key] = l1

input_string = input("Enter a list of values separated by commas: ")
colors = input_string.split(",")

assignment = {}
domains = {}
for region in regions:
    domains[region] = [i for i, color in enumerate(colors)]

# Create the GUI
root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

grid = [[0 for _ in range(5)] for _ in range(len(regions))]

# Draw the initial grid
draw_grid()

# Run the coloring algorithm when the user clicks the button
button = tk.Button(root, text="Color Map", command=color_map)
button.pack()

root.mainloop()
