import BlockNetwork
import Blocks
from abc import ABC, abstractmethod
# from enum import Enum, auto


# class BlockType(Enum):
#     """
#     An enum that lists all types of blocks in the system
#     """
#     CONSTANT = auto()
#     PLUS = auto()
#     MINUS = auto()
#     MULTIPLY = auto()
#     DIVISION = auto()
#     POWER = auto()
#     LT = auto()  # Less Than (<)
#     LTE = auto()  # Less Than or Equals (<=)
#     GT = auto()  # Greater Than (>)
#     GTE = auto()  # Greater Than or Equals (>=)
#     EQ = auto()  # Equals (==)
#     NEQ = auto()  # Not Equals (!=)
#     MOVE = auto()  # Move Block
#     MULTIPLEX = auto()


class BlockFactory:
    """
    Class that uses the factory design pattern to create Block objects
    """
    def __init__(self):
        # a dictionary of different known block classes, and extra operator if necessary
        self._block_classes = {
            "CONSTANT": (Blocks.ConstantBlock,),
            "PLUS": (Blocks.PlusBlockAny,),
            "MINUS": (Blocks.SimpleMathBlock, "-"),
            "MUL": (Blocks.SimpleMathBlock, "*"),
            "DIV": (Blocks.SimpleMathBlock, "/"),
            "POWER": (Blocks.PowerBlock,),
            "LT": (Blocks.ComparisonBlockParameter, "<"),
            "LTE": (Blocks.ComparisonBlockParameter, "<="),
            "GT": (Blocks.ComparisonBlockParameter, ">"),
            "GTE": (Blocks.ComparisonBlockParameter, ">="),
            "EQ": (Blocks.ComparisonBlockParameter, "=="),
            "NEQ": (Blocks.ComparisonBlockParameter, "!="),
            "MOVE": (Blocks.MoveBlockParameter,),
            "MULTIPLEX": (Blocks.MultiplexBlock,),
        }

    def register_block_class(self, key: str, block_class) -> None:
        """
        Register a new type of Block to the factory
        param key: the "name" of your block,
        param block_class: a tuple of (class that implements your block derived from Block,   extra operator parameter)
        note: if block_class is not inside a tuple, it will be put inside one
        """
        bc = block_class
        if type(bc) != tuple:
            bc = (bc,)
        self._block_classes[key] = bc

    def create_block(self, block_type: str, **kwargs) -> Blocks:
        """
        Class that creates a block based on the given BlockType
        param block_type: the type of block to create
        param **kwargs: input args that the block uses
        """
        blocktuple = self._block_classes.get(block_type)
        if not blocktuple:
            e = '"' + str(block_type) + "\" is not a registered block type in the BlockFactory"
            raise KeyError(e)
        if len(blocktuple) > 1:
            return blocktuple[0](operator=blocktuple[1], **kwargs)
        else:
            return blocktuple[0](**kwargs)


# class BlockBuilder(ABC):
#     @abstractmethod
#     def create_block(self):
#         pass
#
#
# class ConstantBlockBuilder(BlockBuilder):
#     def create_block(self, **kwargs):
#         return Blocks.ConstantBlock(**kwargs)
#
#
# class MinusBlockBuilder(BlockBuilder):
#     def create_block(self, **kwargs):
#         return Blocks.SimpleMathBlock(Blocks.minus, **kwargs)


def test_block_factory() -> int:
    # Function that tests blocks to see if they correctly generate
    print("## Starting test BlockFactory")
    # -- TEST INDIVIDUAL BLOCKS
    f = BlockFactory()

    c_1 = f.create_block("CONSTANT", value=2)
    assert(type(c_1) == Blocks.ConstantBlock)
    p = f.create_block("PLUS")
    assert(type(p) == Blocks.PlusBlockAny)

    f.register_block_class("PEEPO", Blocks.ConstantBlock)
    c_2 = f.create_block("PEEPO", value=3)
    assert(type(c_2) == Blocks.ConstantBlock)

    mi = f.create_block("MINUS")
    mul = f.create_block("MUL")
    div = f.create_block("DIV")
    powr = f.create_block("POWER")
    lt = f.create_block("LT")
    lte = f.create_block("LTE")
    gt = f.create_block("GT")
    gte = f.create_block("GTE")
    eq = f.create_block("EQ")
    neq = f.create_block("NEQ")
    mv = f.create_block("MOVE")
    multiplex = f.create_block("MULTIPLEX")

    # -- TEST POW NETWORK --
    network = BlockNetwork.BlockNetwork()
    block_pow = f.create_block("POWER")
    block_const_6 = f.create_block("CONSTANT", value=6)
    block_const_9 = f.create_block("CONSTANT", value=9)

    network.add_block(block_pow, 0, True)
    network.add_block(block_const_6, 0)
    network.add_block(block_const_9, 0)
    assert(network.exec()[0] == 10077696)

    print("## Finished test BlockFactory")
    return 0


test_block_factory()
