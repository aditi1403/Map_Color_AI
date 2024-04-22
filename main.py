import copy
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
    # print(l1)
# print(regions)
input_string = input("Enter a list of values separated by commas: ")
colors = input_string.split(",")
# print(colors)
assignment = {}

# Define the domains for each variable (region)
domains = {}
for region in regions:
    domains[region] = colors.copy()

# Define the MRV heuristic
# print(domains)
def mrv(assignment, domains):
    unassigned_vars = [var for var in domains if var not in assignment]
    if not unassigned_vars:
        return None
    return min(unassigned_vars, key=lambda var: len(domains[var]))

# Define the LCV heuristic
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

# Define the degree heuristic
def degree(var, assignment, regions):
    return len(regions[var])

# Define the forward checking function
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


# Run the forward checking algorithm
result = forward_checking(assignment, domains, regions)

# Print the result
if result is None:
    print('No solution found.')
else:
    print(result)

