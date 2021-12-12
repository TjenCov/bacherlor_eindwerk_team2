import tkinter as tk


imagedata = '''
    R0lGODlhEAAQAOeSAKx7Fqx8F61/G62CILCJKriIHM+HALKNMNCIANKKANOMALuRK7WOVLWPV9eR
    ANiSANuXAN2ZAN6aAN+bAOCcAOKeANCjKOShANKnK+imAOyrAN6qSNaxPfCwAOKyJOKyJvKyANW0
    R/S1APW2APW3APa4APe5APm7APm8APq8AO28Ke29LO2/LO2/L+7BM+7BNO6+Re7CMu7BOe7DNPHA
    P+/FOO/FO+jGS+/FQO/GO/DHPOjBdfDIPPDJQPDISPDKQPDKRPDIUPHLQ/HLRerMV/HMR/LNSOvH
    fvLOS/rNP/LPTvLOVe/LdfPRUfPRU/PSU/LPaPPTVPPUVfTUVvLPe/LScPTWWfTXW/TXXPTXX/XY
    Xu/SkvXZYPfVdfXaY/TYcfXaZPXaZvbWfvTYe/XbbvHWl/bdaPbeavvadffea/bebvffbfbdfPvb
    e/fgb/Pam/fgcvfgePTbnfbcl/bfivfjdvfjePbemfjelPXeoPjkePbfmvffnvbfofjlgffjkvfh
    nvjio/nnhvfjovjmlvzlmvrmpvrrmfzpp/zqq/vqr/zssvvvp/vvqfvvuPvvuvvwvfzzwP//////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////yH+FUNyZWF0ZWQgd2l0aCBU
    aGUgR0lNUAAh+QQBCgD/ACwAAAAAEAAQAAAIzAD/CRxIsKDBfydMlBhxcGAKNIkgPTLUpcPBJIUa
    +VEThswfPDQKokB0yE4aMFiiOPnCJ8PAE20Y6VnTQMsUBkWAjKFyQaCJRYLcmOFipYmRHzV89Kkg
    kESkOme8XHmCREiOGC/2TBAowhGcAyGkKBnCwwKAFnciCAShKA4RAhyK9MAQwIMMOQ8EdhBDKMuN
    BQMEFPigAsoRBQM1BGLjRIiOGSxWBCmToCCMOXSW2HCBo8qWDQcvMMkzCNCbHQga/qMgAYIDBQZU
    yxYYEAA7
'''
class Board(tk.Frame):
    def __init__(self, root, rows = 10, columns = 10):
        self.rows = rows
        self.columns = columns
        self.board = []
        for row in range(self.rows):
            self.board.append([])
            for column in range(self.columns):
                self.board[-1].append([])

############################################# Grafisch
        self.size = 32
        canvas_width = columns * self.size
        canvas_height = rows * self.size
        self.color1 = "white"
        self.color2 = "blue"


        self.pieces = {}

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if parentthe user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addObstacles(self, name, extra, start:(int, int), end:(int, int) = (-1, -1)):
        if end == (-1, -1):
            self.addObstacle(name, extra,start)
        else:
            for x in range(start[0], end[0]):
                for y in range(start[1], end[1]):
                    self.addObstacle(name,extra, (x, y))

    def addObstacle(self, name, extra, coord:(int, int)):
        print(coord[1], coord[0])
        if coord[0]<self.rows and coord[1]< self.columns:
            if len(self.board[coord[0]][coord[1]]) == 0: # deze nog weg?
                self.board[coord[0]][coord[1]].append(name)

                ###################""
                self.canvas.create_image(0, 0, image=extra, tags=(name, "piece"), anchor="c")
                self.placepiece(name, coord[0], coord[1])


    def removeObstacle(self, coord:(int, int)):
        if coord[0]<self.rows and coord[1]< self.columns:
            if len(self.board[coord[0]][coord[1]]) != 0:
                self.board[coord[0]][coord[1]] = []


    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def getBoard(self):
        return self.board
if __name__ == "__main__":
    root = tk.Tk()

    board = Board(root, 8, 8)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = tk.PhotoImage(data=imagedata)

    board.addObstacles("finish", player1, (1, 1))
    board.removeObstacle((3,3))
    print(board.getBoard())
    root.mainloop()
