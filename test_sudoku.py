import pytest
from Sudoku import *


def test_ConvertToSets():
    ary = [[0, 1, 2], [1, 0, 2], [0, 1, 0]]
    s = set(range(1, 10))
    assert convertToSets(ary) == [[s, {1}, {2}], [{1}, s, {2}], [s, {1}, s]]
    assert type(ary[0][0]) is int, "The original array has been changed."
    ary = [[0]]
    assert convertToSets(ary) == [[s]]

def testConvertToInts():
    sets = [[{1, 2}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{2, 3}, {2}, {3}]]
    assert convertToInts(sets) == [[0, 3, 4], [1, 0, 2], [0, 2, 3]]
    assert type(sets[0][0]) is set, "The original array has been changed."
    # Test empty set returns 0
    sets = [[{1, 2}, {5}, {}]]
    assert convertToInts(sets) == [[0, 5, 0]]

def testGetRowLocations():
    lst = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)]
    assert set(lst) == set(getRowLocations(5))
    lst = [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)]
    assert set(lst) == set(getRowLocations(3))
    lst = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
    assert set(lst) == set(getRowLocations(8))

def testGetColumnLocations():
    lst = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5)]
    assert set(lst) == set(getColumnLocations(5))
    lst = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3)]
    assert set(lst) == set(getColumnLocations(3))
    lst = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
    assert set(lst) == set(getColumnLocations(8))

def testGetBoxLocations():
    lst = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
    assert set(lst) == set(getBoxLocations((3, 2)))
    lst = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]
    assert set(lst) == set(getBoxLocations((8, 1)))
    lst = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert set(lst) == set(getBoxLocations((0, 0)))

def testEliminate():
    sets = [[{1, 2}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{2, 3}, {2}, {1, 2, 3}]]
    location = (1, 2) # contains {2}
    count = eliminate(sets, location, [(0, 0), (1, 0), (2, 2)])
    assert count == 2
    assert sets == [[{1}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{2, 3}, {2}, {1, 3}]]
    sets = [[{1, 1}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{1, 3}, {2}, {1, 1, 3}]]
    location = (1, 2) # contains {2}
    count = eliminate(sets, location, [(0, 0), (1, 0), (2, 2)])
    assert count == 0 # No changes should be made
    assert sets == [[{1, 1}, {3}, {4}], [{1}, {3, 5, 7}, {2}], [{1, 3}, {2}, {1, 1, 3}]]

def testIsSolved():
    # Just check whether every cell has been reduced to one number
    array = [[{1}] * 9] * 9
    assert (all([len(array[r][c]) == 1 for r in range(0, 9)
                                               for c in range(0, 9)])) == True
    # modify a location to contain more than one number
    array[3][5] = {1, 2}
    assert (all([len(array[r][c]) == 1 for r in range(0, 9)
                                                for c in range(0, 9)])) == False

    def testSolve(self):
        # Easy
        sudoku1 = [[4, 0, 0,  0, 0, 3,  0, 7, 0],
                   [0, 0, 1,  0, 0, 9,  5, 0, 8],
                   [0, 0, 0,  6, 0, 8,  4, 1, 3],

                   [0, 1, 0,  9, 0, 0,  3, 0, 0],
                   [0, 0, 0,  0, 5, 0,  0, 0, 0],
                   [0, 0, 4,  0, 0, 6,  0, 8, 0],

                   [7, 9, 2,  8, 0, 5,  0, 0, 0],
                   [3, 0, 5,  4, 0, 0,  9, 0, 0],
                   [0, 4, 0,  2, 0, 0,  8, 0, 5]]

        solved1 = [[4, 6, 8,  5, 1, 3,  2, 7, 9],
                   [2, 3, 1,  7, 4, 9,  5, 6, 8],
                   [5, 7, 9,  6, 2, 8,  4, 1, 3],

                   [6, 1, 7,  9, 8, 2,  3, 5, 4],
                   [8, 2, 3,  1, 5, 4,  7, 9, 6],
                   [9, 5, 4,  3, 7, 6,  1, 8, 2],

                   [7, 9, 2,  8, 3, 5,  6, 4, 1],
                   [3, 8, 5,  4, 6, 1,  9, 2, 7],
                   [1, 4, 6,  2, 9, 7,  8, 3, 5]]
        # Easy
        sudoku2 = [[0, 0, 0,  7, 0, 0,  6, 8, 9],
                   [3, 0, 8,  0, 0, 0,  2, 0, 0],
                   [0, 0, 0,  8, 1, 0,  0, 4, 0],

                   [6, 0, 0,  0, 0, 0,  8, 0, 4],
                   [8, 0, 0,  3, 4, 9,  0, 0, 5],
                   [7, 0, 5,  0, 0, 0,  0, 0, 3],

                   [0, 8, 0,  0, 7, 6,  0, 0, 0],
                   [0, 0, 7,  0, 0, 0,  1, 0, 8],
                   [9, 5, 1,  0, 0, 8,  0, 0, 0]]

        solved2 = [[1, 2, 4,  7, 5, 3,  6, 8, 9],
                   [3, 7, 8,  9, 6, 4,  2, 5, 1],
                   [5, 9, 6,  8, 1, 2,  3, 4, 7],

                   [6, 3, 9,  5, 2, 7,  8, 1, 4],
                   [8, 1, 2,  3, 4, 9,  7, 6, 5],
                   [7, 4, 5,  6, 8, 1,  9, 2, 3],

                   [4, 8, 3,  1, 7, 6,  5, 9, 2],
                   [2, 6, 7,  4, 9, 5,  1, 3, 8],
                   [9, 5, 1,  2, 3, 8,  4, 7, 6]]

        # Hard
        sudoku3 = [[9, 0, 0,  0, 0, 8,  0, 0, 0],
                   [0, 0, 0,  0, 3, 2,  0, 0, 0],
                   [6, 8, 0,  9, 0, 1,  0, 7, 0],

                   [8, 0, 9,  5, 2, 0,  0, 3, 0],
                   [2, 0, 0,  0, 0, 0,  0, 0, 5],
                   [0, 4, 0,  0, 9, 3,  7, 0, 8],

                   [0, 2, 0,  3, 0, 9,  0, 6, 4],
                   [0, 0, 0,  2, 8, 0,  0, 0, 0],
                   [0, 0, 0,  6, 0, 0,  0, 0, 3]]

        solved3 = [[9, 0, 0,  0, 0, 8,  0, 0, 0],
                   [0, 0, 0,  0, 3, 2,  0, 0, 0],
                   [6, 8, 0,  9, 0, 1,  0, 7, 2],

                   [8, 0, 9,  5, 2, 0,  0, 3, 0],
                   [2, 0, 0,  0, 0, 0,  0, 0, 5],
                   [5, 4, 6,  1, 9, 3,  7, 2, 8],

                   [0, 2, 0,  3, 0, 9,  0, 6, 4],
                   [0, 0, 0,  2, 8, 0,  0, 0, 0],
                   [0, 0, 0,  6, 0, 0,  0, 0, 3]]

        # Can the solution solve The Times Daily Sudoku (Easy)?
        times_easy = [[7, 0, 1,  0, 0, 4,  9, 6, 0],
                   [9, 0, 2,  0, 0, 5,  0, 4, 0],
                   [5, 0, 0,  3, 0, 0,  2, 7, 0],

                   [0, 1, 6,  2, 0, 0,  7, 0, 0],
                   [0, 8, 0,  0, 6, 0,  3, 0, 2],
                   [2, 0, 0,  7, 0, 3,  1, 0, 0],

                   [0, 9, 0,  0, 1, 7,  0, 0, 8],
                   [8, 0, 4,  5, 0, 9,  0, 0, 7],
                   [0, 7, 0,  0, 8, 0,  0, 3, 9]]

        times_solved = [[7, 3, 1,  8, 2, 4,  9, 6, 5],
                   [9, 6, 2,  1, 7, 5,  8, 4, 3],
                   [5, 4, 8,  3, 9, 6,  2, 7, 1],

                   [3, 1, 6,  2, 5, 8,  7, 9, 4],
                   [4, 8, 7,  9, 6, 1,  3, 5, 2],
                   [2, 5, 9,  7, 4, 3,  1, 8, 6],

                   [6, 9, 3,  4, 1, 7,  5, 2, 8],
                   [8, 2, 4,  5, 3, 9,  6, 1, 7],
                   [1, 7, 5,  6, 8, 2,  4, 3, 1]]



        tryToSolve(sudoku1, solved1)
        tryToSolve(sudoku2, solved2)
        tryToSolve(sudoku3, solved3)
        tryToSolve(times_easy, times_solved)

    def tryToSolve(problem, solution):
        # print_sudoku(problem)
        problemAsSets = convertToSets(problem)
        solve(problemAsSets)
        solved = convertToInts(problemAsSets)
        assert solution == solved
