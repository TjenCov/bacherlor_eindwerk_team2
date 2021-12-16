from BlockNetwork import BlockNetwork
from Blocks import Block, PowerBlock, ConstantBlock, PlusBlockAny, MoveBlockParameter, ComparisonBlockParameter, CheckSolutionBlock

def test_addition():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING 4 + 20 ===")
    block_plus = PlusBlockAny()
    block_const_4 = ConstantBlock(value=4)
    block_const_20 = ConstantBlock(value=20)

    print("\t- Added plus block to network")
    network.add_block(block_plus, 0, True)
    print("\t- Added constant 4 block to network")
    network.add_block(block_const_4, 0)
    print("\t- Added constant 20 block to network")
    network.add_block(block_const_20, 0)

    network.remove_block(block_plus.ID)
    network.remove_block(block_const_4.ID)
    network.remove_block(block_const_20.ID)


    print("EXPEDTED OUTPUT: [24]", "\tNETWORK OUTPUT: ", network.exec())
    print("\n#######################################################################################################\n")

def test_pow():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING 6^9 ===")
    block_pow = PowerBlock()
    block_const_6 = ConstantBlock(value=6)
    block_const_9 = ConstantBlock(value=9)

    print("\t- Added power block to network")
    network.add_block(block_pow, 0, True)
    print("\t- Added constant 6 block to network")
    network.add_block(block_const_6, 0)
    print("\t- Added constant 9 block to network")
    network.add_block(block_const_9, 0)

    print("EXPEDTED OUTPUT: [10077696]", "\tNETWORK OUTPUT: ", network.exec())
    print("\n#######################################################################################################\n")

def test_removal_block_link():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING 5 + 10 + 15 WITH BLOCK 5 REMOVED ===")
    block_plus = PlusBlockAny()
    block_const_5 = ConstantBlock(value=5)
    block_const_10 = ConstantBlock(value=10)
    block_const_15 = ConstantBlock(value=15)

    print("\t- Added plus block to network")
    network.add_block(block_plus, 0, True)
    print("\t- Added constant 5 block to network")
    network.add_block(block_const_5, block_plus.ID)
    print("\t- Added constant 10 block to network")
    network.add_block(block_const_10, block_plus.ID)
    print("\t- Added constant 15 block to network")
    network.add_block(block_const_15, block_plus.ID)

    print("\t- Removed constant 5 block to network")
    network.remove_link(block_plus.getID(), block_const_5.getID())
    network.remove_block(block_const_5.ID)

    print("EXPEDTED OUTPUT: [25]", "\tNETWORK OUTPUT:", network.exec())
    print("\n#######################################################################################################\n")

def test_move():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING BLOCK MOVEMENT ===")
    move_block = MoveBlockParameter()

    print("\t- Added move block to network with initial coordinates [1, 1]")
    network.add_block(move_block, 0)

    print("\t- Move block one up")
    print(move_block.compute(**{"initial_coordinates": [1, 1]}))

    print("\n#######################################################################################################\n")

def test_all():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== ((9 + 3) + (10 + 7))^2 ===")
    block_pow = PowerBlock()
    block_plus_1 = PlusBlockAny()
    block_const_2 = ConstantBlock(value=2)

    block_plus_2 = PlusBlockAny()
    block_const_9 = ConstantBlock(value=9)
    block_const_3 = ConstantBlock(value=3)

    block_plus_3 = PlusBlockAny()
    block_const_10 = ConstantBlock(value=10)
    block_const_7 = ConstantBlock(value=7)

    print("\t- Added power block to network")
    network.add_block(block_pow, 0, True)
    print("\t- Added plus block which contains the output of (9 + 3) + (10 + 7) to network")
    network.add_block(block_plus_1, block_pow.ID, False)
    print("\t- Added constant 2 block to the network which serves as the exponent for the power block")
    network.add_block(block_const_2, block_pow.ID, False)

    print("\n")

    print("\t- Added plus block to network")
    network.add_block(block_plus_2, block_plus_1.ID, False)
    print("\t- Added constant 9 block to network")
    network.add_block(block_const_9, block_plus_2.ID, False)
    print("\t- Added constant 3 block to network")
    network.add_block(block_const_3, block_plus_2.ID, False)

    print("\n")

    print("\t- Added plus block to network")
    network.add_block(block_plus_3, block_plus_1.ID, False)
    print("\t- Added constant 10 block to network")
    network.add_block(block_const_10, block_plus_3.ID, False)
    print("\t- Added constant 7 block to network")
    network.add_block(block_const_7, block_plus_3.ID, False)

    print("EXPEDTED OUTPUT: [841]", "\tNETWORK OUTPUT:", network.exec())
    print("\n#######################################################################################################\n")

def test_comparison():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING 5 == 10 ===")
    block_comp = ComparisonBlockParameter()
    block_const_5 = ConstantBlock(value=5)
    block_const_10 = ConstantBlock(value=10)

    print("\t- Added comparison block to network")
    network.add_block(block_comp, 0, True)
    print("\t- Added constant 5 block to network")
    network.add_block(block_const_5, block_comp.ID)
    print("\t- Added constant 10 block to network")
    network.add_block(block_const_10, block_comp.ID)

    print("EXPEDTED OUTPUT: [0]", "\tNETWORK OUTPUT:", network.exec())
    print("\n#######################################################################################################\n")


def test_check_solution_1():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING CHECKSOLUTION 15==15 ===")
    block_add = PlusBlockAny()
    block_const_5 = ConstantBlock(value=5)
    block_const_10 = ConstantBlock(value=10)
    block_checksolution = CheckSolutionBlock(true_result=15)

    print("\t- Added adder block to network")
    network.add_block(block_add, 0, True)
    print("\t- Added constant 5 block to network")
    network.add_block(block_const_5, 0)
    print("\t- Added constant 10 block to network")
    network.add_block(block_const_10, 0)
    print("\t- Added solution checker block to network (res:15)")
    network.add_block(block_checksolution, block_add.ID, True)
    print("\t- Coupled adder block to solution checker block")
    network.add_link(block_checksolution.getID(), block_add.getID())

    # 15 == 15 dus expect True (dus 1)
    print("EXPECTED OUTPUT: [1]", "\tNETWORK OUTPUT:", network.exec())
    print("\n#######################################################################################################\n")
#
def test_check_solution_2():
    network = BlockNetwork()

    print("\n#######################################################################################################\n")
    print("=== TESTING CHECKSOLUTION 15==23 ===")
    block_add = PlusBlockAny()
    block_const_5 = ConstantBlock(value=5)
    block_const_10 = ConstantBlock(value=10)
    block_checksolution = CheckSolutionBlock(true_result=23)

    print("\t- Added adder block to network")
    network.add_block(block_add, 0, True)
    print("\t- Added constant 5 block to network")
    network.add_block(block_const_5, block_add.ID)
    print("\t- Added constant 10 block to network")
    network.add_block(block_const_10, block_add.ID)
    print("\t- Added solution checker block to network (res:15)")
    network.add_block(block_checksolution, 0, True)
    print("\t- Coupled adder block to solution checker block")
    network.add_link(block_checksolution.getID(), block_add.getID())

    # 15 != 23 dus expect False (dus 0)
    print("EXPECTED OUTPUT: [0]", "\tNETWORK OUTPUT:", network.exec())
    print("\n#######################################################################################################\n")

if __name__ == '__main__':
    test_addition()
    test_removal_block_link()
    test_pow()
    test_move()
    test_all()
    test_comparison()
    test_check_solution_1()
    test_check_solution_2()


