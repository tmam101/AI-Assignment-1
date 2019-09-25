class RowColumn:
    usedValues = None
    idNumber = None

    def __init__(self, idNumber):
        self.usedValues = set()
        self.idNumber = idNumber

    def isValueValid(self, value):
        return value not in self.usedValues

    def addValue(self, value):
        # TODO Here its considering this a dict rather than a set
        self.usedValues.add(value)

    def removeValue(self, value):
        self.usedValues.remove(value)