from main import Block, PowerBlock, ConstantBlock, PlusBlockAny


class BlockNetwork:
    """
    A class representing a network of executable blocks. The network starts by calling upon the execute of the predecessors
    of the rootBlock and then using their output in its own execution.
    """
    def __init__(self, rootBlock):
        self.root = rootBlock

    def exec(self):
        """
        Calls the execute function of the rootBlock. This starts the chain of executes.
        :return:
        """
        self.root.execute()

    def add_block(self, block, parentBlock):
        """
        Adds a block to the network by assigning a pointer from it's desired parentBlock to said block.
        :param block: The block that is to be added to the network
        :param parentBlock: The block representing the parent(execute caller) of the to be added block
        :return:
        """
        parentBlock.add_successor(block)

    def remove_block(self, block):
        """
        Removes a block from the network by removing all existing pointers to this block from all the predecessors lists
        :param block: the block that is to be removed
        :return:
        """

        # TODO: implement(maybe by a bfs? consider adding ID's to the blocks for later ease)
        pass
