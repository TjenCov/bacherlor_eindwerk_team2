from abc import ABC, abstractmethod


def listToKwarg(args, keys):
    """
    Assuming that the input port names of a block are not known, but the order in which inputs are given to the block is
    known, this function converts the list of input values to a dictionary {input_name : input_value}.
    It is assumed that args and keys have the same length
    :param args: values that a block receives as input (list)
    :param keys: block input port names (list of strings)
    """
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
    """
    A block has a list of keyworded inputs, a function that can be executed with these inputs, and outputs the result of
    this function.
    :param function: function that this block represents
    :param inputs: list of strings of input port names. Could be used to display input port names if they do not have the
        same function (like power), can be used to check if correct amount of inputs is given
    :param can_edit: parameters/input ports should not be changed after construction if this is false.
        This is not currently enforced.
    """
    def __init__(self, function, inputs, can_edit=True):
        self.function = function
        self.inputs = inputs
        self.ID = None
        self.can_edit = can_edit
        self.predecessors = []

    @abstractmethod
    def compute(self, **kwargs):
        """
        Function that this block executes. Abstract method, has to be implemented by subclass.
        Use of kwargs allows blocks with any number of inputs to be created.
        If the function called by compute() also supports kwargs, blocks with a
        variable amount of arguments are possible
        (for example, a single add block could be used to add  2 or three numbers)
        :param **kwargs: keyworded arguments that can be given to the called function, generally
            key: input port name
            value: value given in this input port
        :return: depends on self.function given in contructor
        """
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
Commands
"""


def power(base, exponent):
    """
    Power of base to exponent
    :param base: base number of the power operation
    :param exponent: exponent of the power operation
    :return: pow(base,exponent)
    """
    return pow(base, exponent)

def division(teller, noemer):
    """
    Simple division between two numbers: teller/noemer
    :param teller: number to be divided
    :param noemer: number to be divided by
    :return: teller/noemer
    """
    return teller / noemer


def minus(positief, negatief):
    """
    Simple minus: positief-negatief
    :param positief:
    :param negatief:
    :return: positief-negatief
    """
    return positief - negatief


def multiply_any_args(**kwargs):
    """
    Multiply any amount of numbers
    :param **kwargs: keys irrelevant, values are the numbers that should be multiplied with each other
    :return: multiplication of all values in **kwargs
    """
    value = 1
    for name, val in kwargs.items():
        value *= val
    return value


def plus_any_args(**kwargs):
    """"
    Add any amount of numbers
    :param **kwargs: keys irrelevant, values are the numbers that should be added to each other
    :return: Addition of all values in **kwargs
    """
    value = 0
    for name, val in kwargs.items():
        value += val
    return value


def constant(value):
    """
    Returns given value of any type. While this function is functionally very simple, it is implemented to make sure
    that blocks follow the command pattern.
    :param value: return this value
    :return: param value
    """
    return value


def simple_comparison(string_operator, left, right):
    """
    Compares two values according to an operator
    :param string_operator: string that contains the comparison operator.
    :param left: value on the left hand side of the comparison
    :param right: value on the right hand side of the comparison
    :return: (left string_operator right)
    """
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


def move_parameter(**kwargs):
    """
    Given an initial 2D position, moves from that position
    :param **kwargs: needs to contain:
        distance (int): distance to move
        direction ("up", "down", "left", "right"): direction to move
        initial (int,int): starting position to move from
    :return: new list of length two
    """
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
    """
    Receives a selector input and an arbitrary amount of other inputs. The selector input decides which other input
    to output.
    :param selection: string containing name of input port containing desired output
    :param **kwargs:
        keys: input port names. selection will try to match one of these.
        values: value to be returned if key matches
    :return: value of **kwargs[selection]
    """
    return kwargs[str(selection)]


def generic_math(operation,in1,in2):
    """
    Does any of +,-,*,/
    :param operation: string that contains the operation.
    :param left: value on the left hand side of the operation
    :param right: value on the right hand side of the operation
    :return: (left operation right)
    """
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


class SimpleMathBlock(Block):
    """
    Does any of +,*,-,/
    """
    def __init__(self, function=generic_math, inputs=None, operator="+"):
        """
        :param function: generic_math, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :param operator: any of "+","-","*","/"
        :return:
        """
        if inputs is None:
            inputs = ["in1", "in2"]
        super().__init__(function, inputs)
        self.operator = operator

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["in1"]: left hand side of self.operator
            kwargs["in2"]: right hand side of self.operator
        :return: (kwargs["in1"] self.operator kwargs["in2"])
        """
        return self.function(self.operator, kwargs["in1"], kwargs["in2"])

    def getOperator(self):
        return self.operator


class MultiplexBlock(Block):
    """
    returns the value from the input port that has the same name as the value of selector input.
    """
    def __init__(self, function=multiplex, inputs=None):
        """
        By default, this creates a conditional where True and False are represented by 1 and 0
        :param function: multiplex, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always contain "selector", can contain any amount of other strings
        :return:
        """
        if inputs is None:
            inputs = ["selector", "0", "1"]
        super().__init__(function, inputs)

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["selector"]: name of input port whose input will be given as output.
            Any amount of other keys can be present in kwargs. These represent input ports, and the selector will pick
            one of them.
        :return: kwargs[kwargs["selector"]]
        """
        return multiplex(kwargs["selector"], **kwargs)


class ComparisonBlockParameter(Block):
    """
    Does a comparison between two values
    """
    def __init__(self, function=simple_comparison, inputs=None, operator="=="):
        """
        :param function: simple_comparison, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :param operator: any of "==","!=",">","<",">=","<="
        :return:
        """
        if inputs is None:
            inputs = ["left", "right"]
        super().__init__(function, inputs)
        self.operator = operator

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["left"]: left hand side of self.operator
            kwargs["right"]: right hand side of self.operator
        :return: (kwargs["in1"] self.operator kwargs["in2"])
        """
        return self.function(self.operator, kwargs["left"], kwargs["right"])

    def getOperator(self):
        return self.operator


class PowerBlock(Block):
    """
    Calculates power of two inputs
    """
    def __init__(self, function=power, inputs=None):
        """
        :param function: power, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :return:
        """
        if inputs is None:
            inputs = ["base", "exponent"]
        super().__init__(function, inputs)

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["base"]: base number of power operation
            kwargs["exponent"]: exponent of power operation
        :return: base^exponent
        """
        return self.function(kwargs["base"], kwargs["exponent"])

    def translate_input(self, int1, int2):
        return {'base': int1, 'exponent': int2}



class PowerBlockParameter(Block):
    """
    Calculates power of an input and a parameter
    """
    def __init__(self, function=power, inputs=None, exponent=2):
        """
        :param function: power, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :param exponent: exponent of power operation executed by this block
        """
        if inputs is None:
            inputs = ["base"]
        super().__init__(function, inputs)
        self.exponent = exponent


    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["base"]: base number of power operation
        :return: base^self.exponent
        """
        return self.function(kwargs["base"], self.exponent)

    def translate_input(self, int1, int2):
        return {'base': int1, 'exponent': int2}

    def getExponent(self):
        return self.exponent


class PlusBlockAny(Block):
    """
    Adds any amount of numbers
    """
    def __init__(self, function=plus_any_args, inputs=None):
        """
        :param function: plus_any_args, should not be changed. If you want a different function, make a new block.
        :param inputs: List of input ports (names irrelevant) that will receive numbers as input.
        :return:
        """
        if inputs is None:
            inputs = ["int1", "int2", "int3"]
        super().__init__(function, inputs)


    def compute(self, **kwargs):
        """
        :param **kwargs: keys irrelevant, values need to be numbers. Size should match self.inputs
        :return: addition of all values in **kwargs
        """
        return self.function(**kwargs)


class ConstantBlock(Block):
    """
    Returns a value
    """
    def __init__(self, function=constant, inputs=None, value=0):
        """
        :param function: plus_any_args, should not be changed. If you want a different function, make a new block.
        :param inputs: Should be empty or None, will not be used even if larger. Needed for call to super.__init__()
        :param value: The value that this block should return
        """
        super().__init__(function, inputs)
        self.value = value


    def compute(self, **kwargs):
        """
        :param **kwargs: only exists to properly override superclass method, not used here.
        :return: self.value
        """
        return self.function(self.value)

    def getValue(self):
        return self.value


class MoveBlockParameter(Block):
    """
    Moves in 2D space
    """
    def __init__(self, function=move_parameter, inputs=None, direction="up", distance=1):
        """
        :param function: move_parameter, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :param: direction: any of "up","down","left","right"
        :param distance: distance to move
        :return:
        """
        if inputs is None:
            inputs = ["initial_coordinates"]
        super().__init__(function, inputs)
        self.direction = direction
        self.distance = distance

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["initial"]: List of length two containing current 2D coordinates
        :return: kwargs["initial"] moved in direction self.direction by self.distance units
        """
        return self.function(
            **{"distance": self.distance, "direction": self.direction, "initial": kwargs["initial_coordinates"]})

    def getDirection(self):
        return self.direction

    def getDistance(self):
        return self.distance


class MoveBlockInput(Block):
    """
    Moves in 2D space
    """
    def __init__(self, function=move_parameter, inputs=None):
        """
        :param function: move_parameter, should not be changed. If you want a different function, make a new block.
        :param inputs: Should always be None (= default), as the compute function here relies on keyworded names.
        :return:
        """
        if inputs is None:
            inputs = ["initial_coordinates","direction","distance"]
        super().__init__(function, inputs)

    def compute(self, **kwargs):
        """
        :param **kwargs:
            kwargs["initial"]: List of length two containing current 2D coordinates
            kwargs["direction"]: any of "up","down","left","right"
            kwargs["distance"]: distance to move
        :return: kwargs["initial"] moved in direction kwargs["direction"] by kwargs["distance"] units
        """
        return self.function(
            **{"distance": kwargs["distance"], "direction": kwargs["direction"], "initial": kwargs["initial_coordinates"]})


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
