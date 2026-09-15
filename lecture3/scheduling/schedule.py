variables = ["A", "B", "C", "D", "E", "F", "G"]
constraints = [    
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")]

def backtrack(assignment):
    if len(assignment) == len(variables):
        return assignment
    
    var = select_unassign_var(assignment)
    for value in ["Monday", "Tuesday", "Wednesday"]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if consistent(new_assignment):
            result = backtrack(new_assignment)
            if result is not None:
                return result
    return None

def select_unassign_var(assignment):
    for variable in variables:
        if variable not in assignment:
            return variable
    return None

def consistent(assignment):
    for (x, y) in constraints:
        if x not in assignment or y not in assignment:
            continue
        if assignment[x] == assignment[y]:
            return False
    return True

solution = backtrack(dict())
print(solution)