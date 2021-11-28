# ~ Readme ~

## Blocks
A block is a class that has a list of input port names, a function, and possibly extra variables. There is an abstract 
Block class that all more specific blocks should inherit from. 

To implement a new block, create the function you want it
to execute, decide what input parameters it needs, and give these as (default) arguments in the subclass constructor. After this, 
you only need to implement the compute() method to ensure that inputs/arguments are passed correctly. Optionally, you 
can add extra parameters to the constructor and set these as class variables.
### API
These are the existing functions that can be called upon by the user for an existing block.
- \_\_init\_\_(function, inputs, **kwargs) Constructs the block with a given function and list of input ports. If implemented in a specific block, extra kwargs can be set as class variables.
- compute(**kwargs) Calls the function contained in the block and returns the output. The compute method is responsible for correctly passing input in case the function you want to run does not support **kwargs.
## Block Network
The block network is the entity that links together a selection of blocks. When executed it will produce an output based upon the blocks and links that are present in the network.
### API
These are the existing functions that can be called upon by the user for an existing network.
- add_block(block, predecessor_id) Add a block to the network and creating a link from its desired predecessor with given id
- remove_block(block_id) Remove a block with given id from the network, deleting all links to/from it
- add_link(block_id, predecessor_id) Add a link from one block to another given their ids
- remove_link(block_id, predecessor_id) Remove a link from a block to another given their ids
- getOutputs() Returns a list of all output blocks
- execute() Execute the network in order to achieve an output

## Testing


