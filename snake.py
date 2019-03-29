import random

class snake:
    def __init__(self, r, c, length=2):
        if (r > 3 and c > 3):
            self.grow = False
            grid = [[" " for j in range(c)] for i in range(r)]
            initRowSnake = 1
            self.length = length
            self.tl = [1, 1]
            self.hd = [1, length]
            for i in range(length):
                grid[1][1 + i] = "r"
            self.grid = grid
        else:
            print("Sorry, r and c must be at least 4 in length")

    def getHdVal(self):
        return self.grid[self.hd[0]][self.hd[1]]

    def setHdVal(self, char):
        self.grid[self.hd[0]][self.hd[1]] = char

    def getNext(self, index):
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
        if char == "r" and self.getHdVal() != "l":
            self.setHdVal(char)
        elif char == "l" and self.getHdVal() != "r":
            self.setHdVal(char)
        elif char == "u" and self.getHdVal() != "d":
            self.setHdVal(char)
        elif char == "d" and self.getHdVal() != "u":
            self.setHdVal(char)

    def generateFood(self):
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

snake = snake(16,16,6)
snake.playGame()
