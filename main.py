from abc import ABC, abstractmethod


# args = values given as input
# keys = input names
def listToKwarg(args, keys):
    dict = {}
    # For each input value
    for i in range(len(args)):
        # map it to next input port
        dict[keys[i]] = args[i]
    return dict


"""
Abstract base block
"""


# Abstract base class for blocks
class Block(ABC):
    # function: function that this block represents
    # inputs = list of strings of input port names. Could be used to display input port names if they do not have the
    # same function (like power), can be used to check if correct amount of inputs is given
    def __init__(self, function, inputs, can_edit=True):
        self.function = function
        self.inputs = inputs
        self.ID = None
        # If not editable: is input or output block (part of level)
        self.can_edit = can_edit
        self.predecessors = []

    # Use of kwargs allows blocks with any number of inputs to be created
    # If the function called by compute() also supports kwargs, blocks with a
    # variable amount of arguments are possible
    # (for example, a single add block could be used to add  2 or three numbers)
    @abstractmethod
    def compute(self, **kwargs):
        pass

    def execute(self):

        input = []
        for predecessor in self.predecessors:
            input.append(predecessor.execute())
        if input:
            return self.compute(**listToKwarg(input, self.inputs))
        else:
            return self.compute()

    def add_predecessor(self, block):
        """
        Adds a block to the successors list of the current block
        :param block: the to be added block
        :return:
        """
        self.predecessors.append(block)

    def getPredecessors(self):
        return self.predecessors

    def getID(self):
        return self.ID


"""
Commands. Python does little/no type checking, abstract command class not needed?
"""


# Power of base to exponent
def power(base, exponent) -> int:
    return pow(base, exponent)


def division(teller, noemer):
    return teller / noemer


def minus(positief, negatief):
    return positief - negatief


# Multiply any amount of numbers
def multiply_any_args(**kwargs):
    value = 1
    for name, val in kwargs.items():
        value *= val
    return value


# Add any amount of numbers
def plus_any_args(**kwargs) -> int:
    value = 0
    for name, val in kwargs.items():
        value += val
    return value


# return a given number
def constant(value):
    return value


def generic_comparison(string_operator, left, right):
    result = 0
    if string_operator == "==":
        result = left == right
    elif string_operator == "<=":
        result = left <= right
    elif string_operator == ">=":
        result = left >= right
    elif string_operator == "!=":
        result = left != right
    elif string_operator == "<":
        result = left < right
    elif string_operator == ">":
        result = left > right
    return int(result)


# kwargs need to contain:
#    distance (int)
#    direction (up, down, left, right, none (as string))
#    initial (int,int)
def move_parameter(**kwargs):
    distance = kwargs.get("distance", 1)
    direction = kwargs.get("direction")
    initial = kwargs.get("initial")
    multiplier = 1
    if direction == "left" or direction == "down":
        multiplier = -1
    if direction == "left" or direction == "right":
        initial[0] += multiplier * distance
    else:
        initial[1] += multiplier * distance
    return initial


def multiplex(selection, **kwargs):
    return kwargs[str(selection)]

def generic_math(operation,in1,in2):
    result = 0
    if operation == "+":
        result = in1 + in2
    elif operation == "-":
        result = in1 - in2
    elif operation == "*":
        result = in1 * in2
    elif operation == "/":
        result = in1 / in2
    return int(result)

"""
Implemented blocks
"""


# Takes two inputs, executes operation on those inputs. Operation is a parameter in the block.
class SimpleMathBlock(Block):
    def __init__(self, function=generic_math, inputs=None, operator="+"):
        if inputs is None:
            inputs = ["in1", "in2"]
        super().__init__(function, inputs)
        self.operator = operator

    def compute(self, **kwargs):
        return self.function(self.operator, kwargs["in1"], kwargs["in2"])

# returns the value from the input port that has the same name as the value of selector input. "selector" input port
# mandatory
class MultiplexBlock(Block):
    def __init__(self, function=multiplex, inputs=None):
        if inputs is None:
            inputs = ["selector", "0", "1"]
        super().__init__(function, inputs)

    def compute(self, **kwargs):
        return multiplex(kwargs["selector"], **kwargs)


class ComparisonBlockParameter(Block):
    def __init__(self, function=generic_comparison, inputs=None, operator="=="):
        if inputs is None:
            inputs = ["left", "right"]
        super().__init__(function, inputs)
        self.operator = operator

    def compute(self, **kwargs):
        return self.function(self.operator, kwargs["left"], kwargs["right"])
    def getOperator(self):
        return self.operator


# One number to the power of another number
class PowerBlock(Block):
    # By default (should always be the case), this block can calculate power of two numbers (function)
    # and has two inputs named base and exponent
    def __init__(self, function=power, inputs=None):
        if inputs is None:
            inputs = ["base", "exponent"]
        super().__init__(function, inputs)

    # Input names matter here, as base and exponent do not have the same role in the calculation
    def compute(self, **kwargs):
        return self.function(kwargs["base"], kwargs["exponent"])

    def translate_input(self, int1, int2):
        return {'base': int1, 'exponent': int2}


# One number to the power of another number
class PowerBlockParameter(Block):
    # By default (should always be the case), this block can calculate power of two numbers (function)
    # and has one input named base.
    def __init__(self, function=power, inputs=None, exponent=2):
        if inputs is None:
            inputs = ["base"]
        super().__init__(function, inputs)
        self.exponent = exponent

    # Input names matter here, as base and exponent do not have the same role in the calculation
    def compute(self, **kwargs):
        return self.function(kwargs["base"], self.exponent)

    def translate_input(self, int1, int2):
        return {'base': int1, 'exponent': int2}


# Add any amount of numbers
class PlusBlockAny(Block):
    # Any list can be given for the inputs parameter, so the user can change the amount of input ports
    def __init__(self, function=plus_any_args, inputs=None):
        if inputs is None:
            inputs = ["int1", "int2", "int3"]
        super().__init__(function, inputs)

    # Because self.function() uses kwargs with any amounts of arguments, it is fine to just pass all kwargs
    def compute(self, **kwargs):
        return self.function(**kwargs)


class ConstantBlock(Block):
    # Blocks can have additional properties, like "value" here.
    def __init__(self, function=constant, inputs=None, value=0):
        super().__init__(function, inputs)
        self.value = value

    # Additional class variables can be passed to the function of the block
    def compute(self, **kwargs):
        return self.function(self.value)

    def getValue(self):
        return self.value


# Uses parameters set in the block to determine direction/distance, only uses input to receive initial coordinates
class MoveBlockParameter(Block):
    def __init__(self, function=move_parameter, inputs=None, direction="up", distance=1):
        if inputs is None:
            inputs = ["initial_coordinates"]
        super().__init__(function, inputs)
        self.direction = direction
        self.distance = distance

    def compute(self, **kwargs):
        return self.function(
            **{"distance": self.distance, "direction": self.direction, "initial": kwargs["initial_coordinates"]})
    def getDirection(self):
        return self.direction
    def getDistance(self):
        return self.distance


if __name__ == '__main__':
    block_plus = PowerBlock()
    block_const_3 = ConstantBlock(value=3)
    block_const_2 = ConstantBlock(value=2)
    # This "connects" outputs of the ConstantBlocks to the inputs of the PlusBlockAny
    print(block_plus.compute(**{"base": block_const_3.compute(), "exponent": block_const_2.compute()}))

    block_anyPlus = PlusBlockAny()  # Accepts 3 arguments by default
    print(block_anyPlus.compute(
        **{"int1": block_const_2.compute(), "int2": block_const_2.compute(), "int3": block_const_3.compute()}))

    moveupone = MoveBlockParameter()
    print(moveupone.compute(
        **{"initial_coordinates": [1, 1]}))
