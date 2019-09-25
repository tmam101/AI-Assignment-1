class Box:
    result = None
    operation = None
    cells = None

    def __init__(self, result, operation):
        self.result = result
        self.operation = operation
        self.cells = []

    def isValueValid(self, value):
        emptyCount = 0
        values = []
        for cell in self.cells:
            if cell.number == 0:
                emptyCount += 1
            else: #todo is this right?
                values.append(cell.number)
        values.append(value)
        if emptyCount > 1:
            return True

        if self.operation == "*":
            starting = 1
            for value in values:
                starting = starting * value
            return starting == int(self.result)
        elif self.operation == "/":
            divisionCheckOne = values[0] / values[1] == int(self.result)
            remainderCheckOne = values[0] % values[1] == 0
            divisionCheckTwo = values[1] / values[0] == int(self.result)
            remainderCheckTwo = values[1] % values[0] == 0
            return (divisionCheckOne and remainderCheckOne) or (divisionCheckTwo and remainderCheckTwo)
        elif self.operation == "+":
            starting = 0
            for value in values:
                starting = starting + value
                truth = starting == int(self.result)
            return truth
        elif self.operation == "-":
            return (values[0] - values[1] == int(self.result)) or (values[1] - values[0] == int(self.result))
        else:
            return False
