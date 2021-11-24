from main import Block, PowerBlock, ConstantBlock, PlusBlockAny


class BlockNetwork:
    """
    A class representing a network of executable blocks. The network starts by calling upon the execute of the predecessors
    of the rootBlock and then using their output in its own execution.
    """
    def __init__(self):
        self._outputs = []
        self._id_counter = 0
        self._blocks = {}

    def exec(self):
        """
        Calls the execute function of the rootBlock. This starts the chain of executes.
        :return:
        """
        result = []
        for output in self._outputs:
            result.append(output.execute())

        return result

    def add_block(self, block, predecessor_id, output=False):
        """
        Adds a block to the network by assigning a pointer from it's desired parentBlock to said block.
        :param block: The block that is to be added to the network
        :param parentBlock: The block representing the parent(execute caller) of the to be added block
        :return:
        """
        block.ID = self._id_counter
        self._blocks[self._id_counter] = block

        if output:
            self._outputs.append(block)
        else:
            parent = self._blocks[predecessor_id]
            parent.add_predecessor(block)



        # increase counter
        self._id_counter += 1

    def remove_block(self, block_id):
        """
        Removes a block from the network by removing all existing pointers to this block from all the predecessors lists
        :param block: the block that is to be removed
        :return:
        """

        # delete block from network
        del self._blocks[block_id]

        # delete block from predecessor lists
        for entry in self._blocks.values():
            for predecessor in entry.predecessors:
                if predecessor.ID == block_id:
                    entry.predecessors.pop(predecessor)




if __name__ == '__main__':
    network = BlockNetwork()
    block_plus = PowerBlock()
    block_const_3 = ConstantBlock(value=3)
    block_const_2 = ConstantBlock(value=2)
    network.add_block(block_plus, 0, True)
    network.add_block(block_const_2, 0)
    network.add_block(block_const_3, 0)
    output = network.exec()

    print('end')
