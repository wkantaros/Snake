import random

class Snake:
    def __init__(self, row, col, initLength=2):
        if (row > 3 and col > 3):
            self.grow = False
            grid = [[" " for j in range(col)] for i in range(row)]
            initRowSnake = 1
            self.length = initLength
            self.tl = [1, 1]
            self.hd = [1, initLength]
            for i in range(initLength):
                grid[1][1 + i] = "r"
            self.grid = grid
            self.generateFood()
        else:
            print("Sorry, r and c must be at least 4 in length")

    def getHdVal(self):
        """
        gets the value associated with the row and col from hd
        """
        return self.grid[self.hd[0]][self.hd[1]]

    def setHdVal(self, char):
        """
        sets the value associated with hd to char

        :param char: the string to set the value of hd to
        """
        self.grid[self.hd[0]][self.hd[1]] = char

    def getNext(self, index):
        """
        gets the next index from a char in the grid

        :param index: the index of char in grid in [row, col] form
        :returns: the next index from respective param
        """
        direction = self.grid[index[0]][index[1]]
        if direction == "r":
            if index[1] + 1 >= len(self.grid[0]):
                raise Exception("r out of bounds")
            return [index[0], index[1] + 1]
        elif direction == "l":
            if index[1] - 1 < 0:
                raise Exception("l out of bounds")
            return [index[0], index[1] - 1]
        elif direction == "u":
            if index[0] - 1 < 0:
                raise Exception("u out of bounds")
            return [index[0] - 1, index[1]]
        elif direction == "d":
            if index[0] + 1 >= len(self.grid):
                raise Exception("d out of bounds")
            return [index[0] + 1, index[1]]

    def move(self):
        """
        moves snake one space
        """
        if (self.grow):
            self.length += 1
            self.grow = False
        else:
            tlTemp = self.tl
            self.tl = self.getNext(self.tl)
            self.grid[tlTemp[0]][tlTemp[1]] = " "
        direction = self.getHdVal()
        nextHd = self.getNext(self.hd)
        if self.grid[nextHd[0]][nextHd[1]] == "*":
            self.grow = True
            self.generateFood()
        elif self.grid[nextHd[0]][nextHd[1]] != " ":
            raise Exception("ran into tail :(")
        self.hd = nextHd
        self.setHdVal(direction)

    def changeDir(self, char):
        """
        changes direction of snake by updating hdValue to that direction

        :param char: character for desired change in direction
        """
        if char == "r" and self.getHdVal() != "l":
            self.setHdVal(char)
        elif char == "l" and self.getHdVal() != "r":
            self.setHdVal(char)
        elif char == "u" and self.getHdVal() != "d":
            self.setHdVal(char)
        elif char == "d" and self.getHdVal() != "u":
            self.setHdVal(char)

    def generateFood(self):
        """
        generates 'food' in a random spot on the board
        """
        r = random.randint(0, len(self.grid) - 1)
        c = random.randint(0, len(self.grid[0]) - 1)
        if (self.grid[r][c] == " "):
            self.grid[r][c] = "*"
        else:
            self.generateFood()

    def __str__(self):
        str = ""
        for row in self.grid:
            for col in row:
                if col == " ":
                    str += "_"
                else:
                    str += col
            str += "\n"
        return str

    def playGame(self):
        self.generateFood()
        print(self)
        while(True):
            try:
                text = input("")
                self.changeDir(text)
                self.move()
                print(self)
            except:
                print("game over\nscore: {}".format(self.length))
                return

snake = Snake(10,16,6)
snake.playGame()
