import numpy as np

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.capacity = rows * cols
        self.bingoBoard = np.zeros((rows,cols))
        self.currentBoard = np.zeros((rows,cols))
        self.defaultLoc = np.array([-1,-1])
        num = 0
        for i in range(rows):
            for j in range(cols):
                num += 1
                self.bingoBoard[i][j] = num
        self.bingoBoard[rows-1][cols-1] = 0
        self.zero = np.zeros(2)
    
    def restore(self,arr,zero):
        self.rows = len(arr)
        self.cols = len(arr[0])
        self.capacity = self.rows * self.cols
        self.bingoBoard = np.zeros((self.rows,self.cols))
        self.currentBoard = arr
        self.defaultLoc = np.array([-1,-1])
        num = 0
        for i in range(self.rows):
            for j in range(self.cols):
                num += 1
                self.bingoBoard[i][j] = num
        self.bingoBoard[self.rows-1][self.cols-1] = 0
        self.zero = zero
        
    def shuffle(self):
        allNums = [i for i in range(self.capacity)]
        for i in range(self.rows):
            for j in range(self.cols):
                k = int(np.random.random()*len(allNums))
                num = allNums.pop(k)
                self.currentBoard[i][j] = num
                if num == 0:
                    self.zero = np.array([i,j]) 

    def show(self):
        sep = "\n"
        for i in range(self.cols):
            sep += "_______"
        sep += "\n"
        disp = sep
        for i in range(self.rows):
            disp += "|"
            for j in range(self.cols):
                disp += " "+str(self.currentBoard[i][j])+" |"
            disp += sep
        return disp

    def at(self, loc):
        return self.currentBoard[loc[0]][loc[1]]
    def assign(self,loc,num):
        self.currentBoard[loc[0]][loc[1]] = num
    
    def locateNum(self, num):
        if num == 0:
            return np.array([self.rows-1, self.cols-1]) 
        r = int((num-1) / self.cols)
        c = num - r * self.cols - 1
        return np.array([r,c])
        
    def bingo(self):
        if self.currentBoard[self.rows-1][self.cols-1] == 0:
            return np.array_equal(self.currentBoard, self.bingoBoard)
        return False
    
    def moveable(self):
        ds = ""
        if self.zero[0] > 0:
            ds += "s"
        if self.zero[0] < self.rows - 1:
            ds += "w"
        if self.zero[1] > 0:
            ds += "d"
        if self.zero[1] < self.cols - 1:
            ds += "a"
        return ds
    
    def moveTarget(self, direction):
        target = np.zeros(2)
        match direction:
            case "w":
                target = self.zero + np.array([1,0])
            case "a":
                target = self.zero + np.array([0,1])
            case "s":
                target = self.zero - np.array([1,0])
            case "d":
                target = self.zero - np.array([0,1])
            case _:
                return target
        return target
    
    def move(self, direction, target):
        nb = self
        if target[0] < 0:
            if direction not in self.moveable():
                return self
            target = self.moveTarget(direction)
        else:
            nb = Board(self.rows, self.cols)
            nb.currentBoard = self.currentBoard.copy()
            nb.zero = self.zero.copy()
        nb.assign(nb.zero, nb.at(target))
        nb.assign(target, 0) 
        nb.zero = target
        return nb
    

def test():
  b = Board(4,4)
  b.shuffle()
  print(b.currentBoard)
  b.move("w",b.defaultLoc)
  print(b.currentBoard)
