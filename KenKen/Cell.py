from RowColumn import RowColumn


class Cell:
    letter = None
    number = None
    box = None
    row = None
    column = None
    validValues = None
    rowColumnLength = None

    def __init__(self, letter, number, box, rowColumnLength):
        self.letter = letter
        self.number = number
        self.box = box
        self.validValues = []
        self.rowColumnLength = rowColumnLength
        for x in range(rowColumnLength):
            self.validValues.append(x+1)

    def assignValue(self, value):
        if self.isValueValid(value):
            self.number = value
            self.row.addValue(value)
            self.column.addValue(value)
            return True
        return False

    # # TODO probably going to be an error.  I don't know if we can edit validValues while we are iterating through it.
    # # Maybe in bestBacktracking we should iterate through a copy of validValues.
    # def bestAssignValue(self, value):
    #     if self.box.isValueValid(value):
    #         self.number = value
    #         self.validValues.remove(value)
    #         return True
    #     return False

    def bestAssignValue(self, value):
        if self.bestIsValueValid(value):
            self.number = value
            self.row.addValue(value)
            self.column.addValue(value)
            return True
        return False

    # def bestRemoveValue(self, value):
    #     self.number = 0
    #     self.validValues.append(value)

    def bestRemoveValue(self, value):
        self.number = 0
        self.row.removeValue(value)
        self.column.removeValue(value)

    def removeValue(self, value):
        self.number = 0
        self.row.removeValue(value)
        self.column.removeValue(value)

    def isValueValid(self, value):
        return self.row.isValueValid(value) and self.column.isValueValid(value) and self.box.isValueValid(value)

    # TODO For best backtracking search
    def bestIsValueValid(self, value):
        return self.row.isValueValid(value) and self.column.isValueValid(value)


