from Box import Box
from Cell import Cell
from RowColumn import RowColumn
import math
import random
import time


class KenKenSolver:
    rowLength = int(raw_input())
    rows = []
    columns = []
    boxes = {}
    cells = []
    backtrackIterations = 0
    bestBacktrackingIterations = 0

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
            operation = numberAndOperation[len(numberAndOperation) - 1]
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
        self.backtrackIterations += 1
        # Base case: reached the end
        if index == len(self.cells):
            self.print_puzzle()
            print(self.backtrackIterations)
            self.clearPuzzle()
            return True
        for i in range(self.rowLength):  # O(n)
            i = i + 1
            if self.cells[index].assignValue(i):  # O(n^2)
                if self.backtrack(index + 1):
                    return True
                else:
                    self.cells[index].removeValue(i)
        return False

    sortedCells = []

    def sortCells(self):
        for i in range(len(self.sortedCells)):
            value = len(self.sortedCells[i].validValues)
            if i < len(self.sortedCells) - 1:
                nextValue = len(self.sortedCells[i+1].validValues)
                if value > nextValue:
                    temp = self.sortedCells[i+1]
                    self.sortedCells[i+1] = self.sortedCells[i]
                    self.sortedCells[i] = temp
                    self.sortCells() #todo probably inefficient

    def bestBacktracking(self, index):
        for key in self.boxes:
            self.boxes[key].getOptions()
        start_time = time.time()
        for cell in self.cells:
            self.sortedCells.append(cell)
        self.sortCells()
        self.bestBacktrackingSearch(self.sortedCells, index)
        print("--- %s seconds ---" % (time.time() - start_time))

    def bestBacktrackingSearch(self, sortedCells, index):
        self.bestBacktrackingIterations += 1
        if index == len(sortedCells):
            self.print_puzzle()
            print(self.bestBacktrackingIterations)
            return True
        self.print_puzzle()
        cell = sortedCells[index]
        options = cell.validValues
        for i in options:
            if cell.assignValue(i):
                if self.bestBacktrackingSearch(sortedCells, index + 1):
                    return True
                else:
                    cell.removeValue(i)
        return False

    def localSearch(self):
        # number of random restarts
        for i in range(1000):
            degrees = 500
            self.assignRandomValues()
            print('current puzzle')
            self.print_puzzle()
            print(' ')
            # evaluate current state
            currEn = self.getConstraintsViolated()
            if currEn == 0:
                self.print_puzzle()
                return 'solution found'
            # store old value and which cell in case of rejection
            # change 1 cell value (neighbor node of slightly different state);
            # check: is this different from old value?
            improving = True
            iterations = 0
            numWorse = 0

            while improving:
                currValCell = self.cells[1].number
                iterations += 1
                if iterations % 5 == 0:
                    degrees = degrees * 0.8
                    print('degrees')
                    print(degrees)
                    print(' ')
                valDiff = False
                cellToPull = random.randint(1, (len(self.columns) ^ 2))
                while not valDiff:
                    self.cells[cellToPull].number = random.randint(1, len(self.columns))
                    if currValCell != self.cells[cellToPull].number:
                        valDiff = True
                # evaluate new state
                # print(iterations)

                nextEn = self.getConstraintsViolated()
                print('next puzzle')
                self.print_puzzle()
                print('constraints violated: ')
                print(nextEn)
                print (' ')
                # if state is better, accept. otherwise, accept based on probability
                if nextEn < currEn:
                    print('next is better')
                    currEn = nextEn
                    numWorse = 0
                else:
                    numWorse += 1
                    if self.getProbabilityAccept(degrees, nextEn) > random.random:
                        currEn = nextEn
                        print('next is worse, accept anyway with prob:')
                        print (self.getProbabilityAccept(degrees, nextEn))
                        print (' ')
                    else:
                        # restore puzzle to former state- neighbor not accepted
                        self.cells[1].number = currValCell
                # if not better after x iterations, random restart but store current best solution
                if numWorse > 100:
                    print ('not improving. random restart now')
                    improving = False
            # if solution not found after x restarts, quit
        print('no solution found')
        return False

    def assignRandomValues(self):
        for cell in self.cells:
            cell.number = random.randint(1, len(self.columns))
        # print('len of columns:')
        # print(len(self.columns))
        return

    def decreaseTemp(self, temp):
        temp = temp * 0.8

    def getProbabilityAccept(self, temp, energy):
        return 1 - (energy / temp)

    def getConstraintsViolated(self):
        invalid = 0
        for cell in self.cells:
            if not (cell.isValueValid(cell.number)):
                invalid += 1
        return invalid