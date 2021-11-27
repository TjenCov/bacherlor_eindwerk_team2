# ~ Readme ~

## Blocks

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


