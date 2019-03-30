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

## animation functions
numRows = 50
numCols = 67
snake = Snake(numRows,numCols,4)

def printBoard():
    for i in range(numRows):
        for j in range(numCols):
            if snake.grid[i][j] != " ":
                fill(#f44242)
                noStroke()
                rect(j*12,i*12,12,12)
                

def gameOver():
    message = "game over\nscore: {}".format(snake.length)
    textSize(24)
    text(message, 10, 20)
    
def setup():
    size(804, 600)
    background(51)
    printBoard()
    frameRate(20)

def draw():
    background(51)
    try:
        printBoard()
        snake.move()
        if (key == CODED):
            if keyCode == UP:
                snake.changeDir("u")
            elif keyCode == DOWN:
                snake.changeDir("d")
            elif keyCode == LEFT:
                snake.changeDir("l")
            elif keyCode == RIGHT:
                snake.changeDir("r")
    except:
        gameOver()
        noLoop()
