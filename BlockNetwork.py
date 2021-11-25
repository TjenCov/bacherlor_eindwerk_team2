import JsonParser
from main import Block, PowerBlock, ConstantBlock, PlusBlockAny, MoveBlockParameter


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

    def _register_block(self, block):
        block.ID = self._id_counter
        self._blocks[self._id_counter] = block

        # increase counter
        self._id_counter += 1

    def add_block(self, block, predecessor_id, output=False):
        """
        Adds a block to the network by assigning a pointer from it's desired parentBlock to said block.
        :param block: The block that is to be added to the network
        :param parentBlock: The block representing the parent(execute caller) of the to be added block
        :return:
        """

        if block.ID is None:
            self._register_block(block)

        if output:
            self._outputs.append(block)
        else:
            parent = self._blocks[predecessor_id]
            parent.add_predecessor(block)

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
                    entry.predecessors.remove(predecessor)


    def add_link(self, block_id, predecessor_id):
        block = self._blocks[block_id]
        predecessor_block = self._blocks[predecessor_id]

        block.add_predecessor(predecessor_block)


    def remove_link(self, block_id, predecessor_id):
        block = self._blocks[block_id]
        for predecessor in block.predecessors:
            if predecessor_id == predecessor.ID:
                block.predecessors.remove(predecessor)

    def getOutputs(self):
        """
        Getter for the outputs variable
        :return: list of Blocks
        """
        return self._outputs

    def getId_counter(self):
        """
        Getter for the id_counter variable
        :return: integer
        """
        return self._id_counter

if __name__ == '__main__':

    move_network = BlockNetwork()
    block_start_position = ConstantBlock(value=[2,3])
    block_move_right_two = MoveBlockParameter(direction="right",distance=2)
    move_network.add_block(block_move_right_two,0,True)
    move_network.add_block(block_start_position, 0)
    print(move_network.exec())
    JsonParser.write("network2.json", move_network)
    #new_move_network = JsonParser.read("network2.json")
    #print(new_move_network.exec())

    network = BlockNetwork()
    block_plus = PlusBlockAny()
    block_power = PowerBlock()
    block_const_3 = ConstantBlock(value=3)
    block_const_2 = ConstantBlock(value=2)
    block_const_5 = ConstantBlock(value=5)

    network.add_block(block_plus, 0, True)
    network.add_block(block_power, 0, True)
    network.add_block(block_const_2, 0)
    network.add_block(block_const_3, 0)
    network.add_block(block_const_3, 1)
    network.add_block(block_const_5, 1)
    network.remove_link(0, 3)
    network.add_link(0, 3)

    JsonParser.write("network.json", network)
    newnetwork = JsonParser.read("network.json")
    newoutput = newnetwork.exec()
    output = network.exec()
    print(output)
    print(newoutput)
    print('end')
