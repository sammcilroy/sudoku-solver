'''
Automatic Sudoku Solver
Python
Sam McIlroy
'''


def read_sudoku(file):
    stream = open(file)
    data = stream.readlines()
    stream.close()
    return eval("".join(data))

def convertToSets(problem):
    return_array = []
    for array in problem:
        this_array = []
        for integer in array:
            if integer == 0: # The cell's true value is still unknown
                this_array.append(set(range(1,10))) # Sudoku cell takes ints 1-9
            elif integer in range(1,10):
                this_array.append({integer}) # Cell value is already known
        return_array.append(this_array)
    return return_array

def convertToInts(problem):
    return_array = []
    for array in problem:
        this_array = []
        for set in array:
            if len(set) > 1: # set contains more than one element
                this_array.append(0)
            elif set == {}: # replace empty set value with 0
                this_array.append(0)
            else:
                for integer in set:
                    this_array.append(integer) # append the single integer to array
        return_array.append(this_array)
    return return_array

def getRowLocations(rowNumber):
    return_array = []
    for i in range(0,9): # for each column in the puzzle
        return_array.append((rowNumber, i)) # return values for the row
    return return_array

def getColumnLocations(columnNumber):
    return_array = []
    for i in range(0,9): # for each row in the puzzle
        return_array.append((i, columnNumber)) # return values for the column
    return return_array

def getBoxLocations(location):
    box_1 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    box_2 = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
    box_3 = [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]

    box_4 = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
    box_5 = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
    box_6 = [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]

    box_7 = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]
    box_8 = [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)]
    box_9 = [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]

    # determine the values of each 3x3 'box' in the puzzle
    if location[0] in range(0,3):
        if location[1] in range(0,3):
            return box_1
        elif location[1] in range(3,6):
            return box_2
        else:
            return box_3

    if location[0] in range(3,6):
        if location[1] in range(0,3):
            return box_4
        elif location[1] in range(3,6):
            return box_5
        else:
            return box_6

    if location[0] in range(6,9):
        if location[1] in range(0,3):
            return box_7
        elif location[1] in range(3,6):
            return box_8
        else:
            return box_9

def eliminate(problem, location, listOfLocations):
    # Determine contents of location
    row = location[0]
    column = location[1]
    contains = list(problem[row][column])[0]
    count = 0
    # remove location from changes
    if location in listOfLocations:
        listOfLocations.remove(location)
    # remove contents of location from others. This number can be eliminated.
    for location in listOfLocations:
        row = location[0]
        column = location[1]
        if contains in problem[row][column]:
            problem[row][column].remove(contains)
            count += 1 # record an elimination has been made

    return count

def isSolved(problem):
    for location in problem:
        for values in location:
            if len(values) > 1: # if any location has more than 1 possible value remaining
                return False # the puzzle has not been completely solved
    return True # otherwise all values have been reduced to one and the puzzle is solved

def solve(problem):
    unsuccessful_count = 0 # keep a count of how many times an elimination has not been made
    while not isSolved(problem):
        # If unsuceesful at eliminations for some time, give up
        if unsuccessful_count > 1000:
            return False # failed to solve the puzzle
        # Else, continue trying to solve the puzzle
        for i in range(0,9):
            for j in range(0,9):
                locations_in_row = getRowLocations((i,j))
                location = (i,j)
                if len(problem[i][j]) == 1:
                    locations_in_row = getRowLocations(location[0])
                    # eliminate based on known values in same row
                    rows = eliminate(problem, location, locations_in_row)
                    locations_in_column = getColumnLocations(location[1])
                    # eliminate based on known values in same column
                    columns = eliminate(problem, location, locations_in_column)
                    box = getBoxLocations(location)
                    # eliminate based on known values in same 'box'
                    boxes = eliminate(problem, location, box)
                    #print(rows+columns+boxes, 'eliminations made')
                    if rows+columns+boxes == 0:
                        # no matches made this loop
                        unsuccessful_count += 1

    return True # successfully solved the puzzle

def print_sudoku(problem):
    # replace 0s with .
    for i in range(0,9):
        for j in range(0,9):
            if problem[i][j] == 0:
                problem[i][j] = '.'

    # convert values to strings for printing
    for i in range(0,9):
        for j in range(0,9):
            problem[i][j] = str(problem[i][j])

    print('+--------+--------+--------+')
    for i in range(0,3):
        print('|', end='')
        print(problem[i][0], ' ', end='')
        print(problem[i][1], ' ', end='')
        print(problem[i][2], '|', end='')
        print(problem[i][3], ' ', end='')
        print(problem[i][4], ' ', end='')
        print(problem[i][5], '|', end='')
        print(problem[i][6], ' ', end='')
        print(problem[i][7], ' ', end='')
        print(problem[i][8], '|')
    print('+--------+--------+--------+')
    for i in range(3,6):
        print('|', end='')
        print(problem[i][0], ' ', end='')
        print(problem[i][1], ' ', end='')
        print(problem[i][2], '|', end='')
        print(problem[i][3], ' ', end='')
        print(problem[i][4], ' ', end='')
        print(problem[i][5], '|', end='')
        print(problem[i][6], ' ', end='')
        print(problem[i][7], ' ', end='')
        print(problem[i][8], '|')
    print('+--------+--------+--------+')
    for i in range(6,9):
        print('|', end='')
        print(problem[i][0], ' ', end='')
        print(problem[i][1], ' ', end='')
        print(problem[i][2], '|', end='')
        print(problem[i][3], ' ', end='')
        print(problem[i][4], ' ', end='')
        print(problem[i][5], '|', end='')
        print(problem[i][6], ' ', end='')
        print(problem[i][7], ' ', end='')
        print(problem[i][8], '|')
    print('+--------+--------+--------+')

def ask_yes_or_no(prompt="Solve another puzzle? (Yes(y) or No(n)): "):
    answer = str(input(prompt))
    if answer.startswith('y') or answer.startswith('Y'):
        return True
    elif answer.startswith('n') or answer.startswith('N'):
        return False
    else:
        print("Please answer Yes(y) or No(n)")
        return ask_yes_or_no()

def main():
    valid_file = False
    while not valid_file:
        try:
            sudoku_file = input('Please enter the name of a file containg a Sudoku puzzle: ')
            problem = read_sudoku(sudoku_file)
            valid_file = True
        except FileNotFoundError:
            print('File not found. Please try again')
    print('')
    print('The inputted puzzle is: ')
    print('')
    print_sudoku(problem) # Print the puzzle to be solved in Sudoku format
    print('')
    print('')
    # Soultion
    problem = read_sudoku(sudoku_file)
    problem = convertToSets(problem) # convert to sets for solve function
    solve(problem)
    if isSolved(problem):
        solved = problem # store the successful solution
        print('The complete solution is:')
        print(' ')
        problem = convertToInts(problem) # convert to ints for printing
        print_sudoku(problem)
        print(' ')
    else:
        failed = problem # store the failed partial solution
        print('The solution could not be completed')
        print(' ')
        print('A partial solution is:')
        print(' ')
        problem = convertToInts(problem) # convert to ints for printing
        print_sudoku(problem)
        print(' ')
        print('Unsolved locations:')
        print('')
        for i in range(0,9):
            for j in range(0,9):
                unsolved_location = (i,j)
                possible_values = failed[i][j]
                if len(possible_values) > 1: # The location has not been completely solved
                    # Print each location and the remaining possible values
                    print('Location', unsolved_location,'might be any of', possible_values)
        print(' ')
        print(' ')




if __name__ == "__main__": main() # Run main once at start
while ask_yes_or_no(): main() # continue to run main() while user anwers yes
