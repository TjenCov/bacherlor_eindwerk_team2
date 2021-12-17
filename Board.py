import json


class Board(tk.Frame):
    def __init__(self, rows = 10, columns = 10):
        """
        initialize the board
        """
        self.rows = rows
        self.columns = columns
        self.board = []
        for row in range(self.rows):
            self.board.append([])
            for column in range(self.columns):
                self.board[-1].append([])

    def addObstacles(self, name, start:(int, int), end:(int, int) = (-1, -1)):
        """
        add obstacles to the board, if an end position is given fill the square between start and end with obstacles
        """
        if end == (-1, -1):
            self.addObstacle(name, start)
        else:
            for x in range(start[0], end[0]):
                for y in range(start[1], end[1]):
                    self.addObstacle(name,(x, y))


    def addObstacle(self, name, coord:(int, int)):
        """
        helperfunction obstacle
        """
        if coord[0]<self.rows and coord[1]< self.columns:
            self.board[coord[0]][coord[1]].append(name)



    def removeObstacle(self, coord:(int, int)):
        """
        remove an obstacle
        """
        if coord[0]<self.rows and coord[1]< self.columns:
            if len(self.board[coord[0]][coord[1]]) != 0:
                self.board[coord[0]][coord[1]] = []

    def getBoard(self):
        """
        getter board
        """
        return self.board

    def _createJsonString(self):
        """
        create a json string
        """
        text = '\"height\": {0},\n' \
               '\"width\": {1},\n' \
               '\"entities\": [\n\t'.format(self.rows, self.columns)

        for row in range(self.rows):
            for column in range(self.columns):
                tile = self.board[row][column]
                if not len(tile) == 0:
                    entity = '\n\t\t\t\"x\": {},\n\t\t\t\"y\": {},\n\t\t\t'.format(column, row)
                    entity_description = '{\n\t\t\t\t'+'\"type\": \"{}\",\n\t\t\t\t\"extra\":[]'.format(tile[0]) + '\n\t\t\t\t}'
                    entity = '\t{' + entity + '\"entity\": {}\n\t'.format(entity_description) + '\t}'
                    if row == self.rows-1 and column == self.columns-1:
                        text += entity + '\n\t'
                    else:
                        text += entity + ',\n\t'

        return '{' + text + ']\n}'

    def to_json(self, filename):
        """
        Parse board to json in provided location
        :param filename: location where map needs to be saved to
        :return: None
        """

        text = self._createJsonString()
        with open(filename, 'w') as file:
            file.write(text)

    def load_json(self, filename):
        """
        load a json file into a board
        """
        with open(filename) as file:
            map = json.load(file)
        rows = map['height']
        columns = map['width']
        board = []
        for row in range(rows):
            board.append([])
            for column in range(columns):
                board[row].append([])

        for entity in map['entities']:
            board[entity['x']][entity['y']].append(entity['entity']['type'])
            board[entity['x']][entity['y']].append(entity['entity']['extra'])

        self.board = board


if __name__ == "__main__":

    board = Board(8, 8)
    board.addObstacles("start", (7, 7))
    board.addObstacles("finish", (1, 1))
    board.removeObstacle((3,3))
    print(board.getBoard())
    board.to_json('testLocation.json')
    board.load_json('testLocation.json')
