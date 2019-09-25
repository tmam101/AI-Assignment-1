from Box import Box
from Cell import Cell
from RowColumn import RowColumn
import math

rowLength = int(raw_input())
rows = []
columns = []
boxes = {}
cells = []

# Create rows and columns
for x in range(rowLength):
    row = RowColumn(x)
    column = RowColumn(x)
    rows.append(row)
    columns.append(column)


def get_input():
    # Get each line of letters
    for x in range(rowLength):
        letters = raw_input()
        # Use each letter in the line to create a cell.  Create the cell list.
        for letter in letters:
            boxes[letter] = "test"
            cell = Cell(letter, 0, None)
            cells.append(cell)
    # Get Letter to Result/Operation mappings.  Create boxes.
    for x in range(len(boxes)):
        lineSections = raw_input().split(':')
        character = lineSections[0]
        numberAndOperation = lineSections[1]
        operation = numberAndOperation[len(numberAndOperation)-1]
        number = numberAndOperation[:-1]
        box = Box(number, operation)
        boxes[character] = box
    # Assign boxes to cells
    for cell in cells:
        box = boxes[cell.letter]
        cell.box = box
        box.cells.append(cell)
    # Assign rows and columns to cells
    for cellIndex in range(len(cells)):
        cells[cellIndex].row = rows[cellIndex / rowLength]
        cells[cellIndex].column = columns[cellIndex % rowLength]


def print_puzzle():
    line = ""
    for i in range(len(cells)):
        if (i % math.sqrt(len(cells)) == 0) and (i != 0):
            print(line)
            line = ""
        line += str(cells[i].number)
    print(line)
    print("")


def clearPuzzle():
    for cell in cells:
        cell.number = 0
    print_puzzle()


# TODO Ensure handling of iteration count is correct
def backtrack(index, iterations):
    # Base case: reached the end
    if index == len(cells):
        print_puzzle()
        print(iterations)
        return True
    for i in range(rowLength):
        i = i + 1
        if cells[index].assignValue(i):
            if backtrack(index + 1, iterations + 1):
                return True
            else:
                cells[index].removeValue(i)
    return False

def bestBacktracking(index):
    if index == len(cells):
        return True



get_input()
backtrack(0, 0)
