import random
# import os 
# os.system("afplay filename")
#from playsound import playsound - this is how to do it if you could in python
#playsound("filename")


class Snake:
    def __init__(self, row, col, initLength=2):
        if (row > 3 and col > 3):
            self.isGoing = True
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
                self.isGoing = False
                raise Exception("r out of bounds")
            return [index[0], index[1] + 1]
        elif direction == "l":
            if index[1] - 1 < 0:
                self.isGoing = False
                raise Exception("l out of bounds")
            return [index[0], index[1] - 1]
        elif direction == "u":
            if index[0] - 1 < 0:
                self.isGoing = False
                raise Exception("u out of bounds")
            return [index[0] - 1, index[1]]
        elif direction == "d":
            if index[0] + 1 >= len(self.grid):
                self.isGoing = False
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
            self.isGoing = False
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

# animation functions
numRows = 50
numCols = 67
counter = [1]
snake = Snake(numRows, numCols, 10)

def printBoard():
    for i in range(numRows):
        for j in range(numCols):
            chars = "uldr"
            if snake.grid[i][j] in chars:
                fill(255, 255, 255)
                noStroke()
                rect(j * 12, i * 12, 12, 12)
            elif snake.grid[i][j] == "*":
                fill(244, 66, 66)
                noStroke()
                rect(j * 12, i * 12, 12, 12)
                
def printBoardInverse():
    for i in range(numRows):
        for j in range(numCols):
            chars = "uldr"
            if snake.grid[i][j] in chars:
                fill(244, 66, 66)
                noStroke()
                rect(j * 12, i * 12, 12, 12)
            elif snake.grid[i][j] == "*":
                fill(255, 255, 255)
                noStroke()
                rect(j * 12, i * 12, 12, 12)
                
def gameOver():
    fill(255, 255, 255)
    message = "game over\nscore: {}".format(snake.length)
    textSize(24)
    text(message, 10, 20)
    counter[0] += 1

def changeDir():
    if (key == CODED):
        if keyCode == UP:
            snake.changeDir("u")
        elif keyCode == DOWN:
            snake.changeDir("d")
        elif keyCode == LEFT:
            snake.changeDir("l")
        elif keyCode == RIGHT:
            snake.changeDir("r")

def setup():
    size(804, 600)
    background(51)
    printBoard()
    frameRate(20)

def draw():
    background(51)
    if counter[0] == 1:
        try:
            changeDir()
            snake.move()
            printBoard()
        except:
            printBoardInverse()
            gameOver()
            frameRate(2)
    elif counter[0] == 2:
        printBoard()
        gameOver()
    elif counter[0] == 3:
        printBoardInverse()
        gameOver()
        noLoop()
