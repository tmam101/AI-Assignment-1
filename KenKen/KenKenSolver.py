from Box import Box
from Cell import Cell
from RowColumn import RowColumn
import math


class KenKenSolver:
    rowLength = int(raw_input())
    rows = []
    columns = []
    boxes = {}
    cells = []
    backtrackIterations = 0

    # Create rows and columns
    for x in range(rowLength):
        row = RowColumn(x)
        column = RowColumn(x)
        rows.append(row)
        columns.append(column)


    def get_input(self):
        # Get each line of letters
        for x in range(self.rowLength):
            letters = raw_input()
            # Use each letter in the line to create a cell.  Create the cell list.
            for letter in letters:
                self.boxes[letter] = "test"
                cell = Cell(letter, 0, None, self.rowLength)
                self.cells.append(cell)
        # Get Letter to Result/Operation mappings.  Create boxes.
        for x in range(len(self.boxes)):
            lineSections = raw_input().split(':')
            character = lineSections[0]
            numberAndOperation = lineSections[1]
            operation = numberAndOperation[len(numberAndOperation)-1]
            number = numberAndOperation[:-1]
            box = Box(number, operation)
            self.boxes[character] = box
        # Assign boxes to cells
        for cell in self.cells:
            box = self.boxes[cell.letter]
            cell.box = box
            box.cells.append(cell)
        # Assign rows and columns to cells
        for cellIndex in range(len(self.cells)):
            self.cells[cellIndex].row = self.rows[cellIndex / self.rowLength]
            self.cells[cellIndex].column = self.columns[cellIndex % self.rowLength]


    def print_puzzle(self):
        line = ""
        for i in range(len(self.cells)):
            if (i % math.sqrt(len(self.cells)) == 0) and (i != 0):
                print(line)
                line = ""
            line += str(self.cells[i].number)
        print(line)
        print("")


    def clearPuzzle(self):
        for cell in self.cells:
            cell.removeValue(cell.number)
        self.backtrackIterations = 0


    # TODO Ensure handling of iteration count is correct
    def backtrack(self, index):
        # Base case: reached the end
        if index == len(self.cells):
            self.print_puzzle()
            print(self.backtrackIterations)
            self.clearPuzzle()
            return True
        for i in range(self.rowLength):  #O(n)
            i = i + 1
            self.backtrackIterations += 1
            if self.cells[index].assignValue(i): #O(n^2)
                if self.backtrack(index + 1):
                    return True
                else:
                    self.cells[index].removeValue(i)
        return False

    def bestBacktracking(self, index, iterations):
        # Base case: reached the end
        if index == len(self.cells):
            self.print_puzzle()
            print(iterations)
            return True
        cell = self.cells[index]
        self. print_puzzle()
        # Rather than iterate from 1 to 6 if there are 6 cells in a row, for example,
        # Iterate only through the numbers that are valid from the start.
        # TODO is this actually more efficient?
        validValues = []
        for i in range(self. rowLength): #O(n)
            i = i + 1
            if cell.row.isValueValid(i) and cell.column.isValueValid(i):
                validValues.append(i)
        for i in validValues: #O(logn)
            iterations += 1
            if cell.assignValue(i): #O(n^2)
                if self.bestBacktracking(index + 1, iterations):
                    return True
                else:
                    cell.removeValue(i)
                    self.print_puzzle()
        return False

    #   Most Constrained Variable:
    #   Goal of 2, 2 cells, (1 1). Goal of 11, (5,6)(6,5).  Goal of 6, (1,5)(5,1)(2,4)(4.2)
    #   Most Constraining variable
    #
    #   Least Constraining value
    #
    #   Filtering or Forward Checking
    #   TODO are we already doing this? We store used numbers in each row and column.
    #   Maybe for this, instead of testing 1-6, just test the valid values for that cell.  But does that actually make it more efficient?
    #   TODO can we use the same cells/boxes/rows for best backtracking, or should we create a new structure with different handling of things?

    # TODO Start at the largest(or smallest) box, recursively go to the smaller(or larger) boxes


    # get_input()
    # backtrack(0, 0)
    # bestBacktracking(0, 0)
    # for cell in cells:
    #     print(cell.validValues)
