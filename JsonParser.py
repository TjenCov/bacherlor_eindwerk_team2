import json
import BlockNetwork

IDdict = {}


def write(filename: str, network: BlockNetwork):
    """
    parses a network and writes it in a json file
    """
    data = {}
    data[f"name"] = f"network"
    networklist = []
    for block in network.getOutputs():
        networklist.append(writeNetwork(block))
    data[f"networklist"] = networklist

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def writeNetwork(block):
    """
    helperfunction for write()
    """
    datadict = {}
    datadict[f"name"] = type(block).__name__

    datadict[f"ID"] = block.getID()
    if type(block).__name__ == "ConstantBlock":
        datadict["value"] = block.getValue()
        return datadict
    elif type(block).__name__ == "MoveBlockParameter":
        datadict["distance"] = block.getDistance()
        datadict["direction"] = block.getDirection()

    elif type(block).__name__ == ("ComparisonBlockParameter" or "SimpleMathBlock"):
        datadict["operator"] = block.getOperator()

    elif type(block).__name__ == "PowerBlockParameter":
        datadict["exponent"] = block.getExponent()

    returnlist = []
    for predecessor in block.getPredecessors():
        returnlist.append(writeNetwork(predecessor))

    datadict["predecessors"] = returnlist
    return datadict


def read(filename: str):
    """
    reads a json and creates a network
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    network = BlockNetwork.BlockNetwork()

    if data["name"] == "network":

        for starterBlock in data[f"networklist"]:
            network = readNetwork(starterBlock, network, -1)
    IDdict.clear()
    return network


def readNetwork(starterBlock, network, networkid):
    """
    helperfunction for readJson()
    """
    outputbool = False
    if networkid == -1:
        networkid = 0
        outputbool = True

    id = starterBlock["ID"]
    if id in IDdict:
        block = IDdict[id]
        network.add_block(block, networkid, outputbool)
        return network
    else:

        if starterBlock["name"] == "ConstantBlock":
            block = getattr(BlockNetwork, starterBlock["name"])(value=starterBlock["value"])
            network.add_block(block, networkid, outputbool)
            IDdict[id] = block
            return network
        elif starterBlock["name"] == ("ComparisonBlockParameter" or "SimpleMathBlock"):
            block = getattr(BlockNetwork, starterBlock["name"])(operator=starterBlock["operator"])

        elif starterBlock["name"] == "MoveBlockParameter":
            block = getattr(BlockNetwork, starterBlock["name"])(direction=starterBlock["direction"], distance=starterBlock["distance"])

        elif starterBlock["name"] == "MoveBlockParameter":
            block = getattr(BlockNetwork, starterBlock["name"])(exponent=starterBlock["exponent"])

        else:
            block = getattr(BlockNetwork, starterBlock["name"])()

    network.add_block(block, networkid, outputbool)
    IDdict[id] = block

    idcounter = network.getId_counter() - 1
    for predecessor in starterBlock["predecessors"]:
        network = readNetwork(predecessor, network, idcounter)
    return network


