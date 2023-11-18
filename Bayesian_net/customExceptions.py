

class ProbTableError(Exception):
    '''
    Exception raised for errors in the Plotting method.
    '''
    def __init__(self, table):
        self.table = table

        self.message = "the probability_table must have exactly two columns"
        super().__init__(self.message)

class Variable_assignmentError(Exception):
    '''
    Exception raised for errors in the Build_ProbTables.assign_evidence method.
    '''
    def __init__(self, variable):
        self.variable = variable

        self.message = f"the variable <{self.variable}> does not exist in the probability table"
        super().__init__(self.message)

class Value_assignmentError(Exception):
    '''
    Exception raised for errors in the Build_ProbTables.assign_evidence method.
    '''
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

        self.message = f"the value <{self.value}> of variable <{self.variable}> does not exist in the probability table"
        super().__init__(self.message)