from board import Board
import numpy as np
import time

def play(r,c):
  b = Board(r,c)
  b.restore(np.array([[1,8,0],[7,2,3],[6,5,4]]),np.array([0,2]))
  #b.shuffle()
  round = 49
  while not(b.bingo()):
    round += 1
    print(b.currentBoard)
    #f = open("window.txt", "w")
    #f.write(str(b.currentBoard)+"\n\n"+str(round))
    #f.close()
    direction = input("第"+str(round)+"步--请输入移动方向： ")
    b.move(direction, b.defaultLoc)
  print("恭喜你成功复原！")
  print(b.currentBoard)

def automatic(r,c,policy,maxTrial):
  b = Board(r,c)
  #b.shuffle()
  b.restore(np.array([[2,0,4],[8,7,5],[1,3,6]]),np.array([0,1]))
  #b.restore(np.array([[1,2,3],[4,5,6],[8,7,0]]),np.array([2,2]))
  orig = b.currentBoard.copy()
  round = 0
  path = ""
  while not(b.bingo()) and round < maxTrial:
    round += 1
    print("---Round", round)
    print(b.currentBoard)
    #f = open("window.txt", "w")
    #f.write(str(b.currentBoard)+"\n\n"+str(round))
    #f.close()
    d = policy(b)
    print("Move:",d)
    b.move(d, b.defaultLoc) 
    path += d
  if b.bingo():
    print(b.currentBoard)
    print("恭喜你成功复原！")
  else:
    print("---Max trial reached---")
  print(path)
  print("Original")
  print(orig)
  print("Final")
  print(b.currentBoard)

def randomize(board):
  ds = board.moveable()
  return ds[int(np.random.random()*len(ds))]

def dist(loc1, loc2):
  return 1.5*np.square(loc1[0] - loc2[0]) + np.square(loc1[1] - loc2[1])
        
def reward(board, target):
  ref = board.locateNum(board.at(target))
  last = np.array([board.rows-1, board.cols-1])
  return dist(target, ref) - dist(board.zero, ref)
  # return 10*dist(target, ref) + dist(board.zero, last) - 10*dist(board.zero, ref) - 10*dist(target, last)

def multiReward(board, steps, discount):
  if steps == 0:
    return 0
  ds = board.moveable()
  totalReward = 0
  for d in ds:
    t = board.moveTarget(d)
    totalReward += reward(board, t)
    nb = board.move("", t)
    totalReward += discount * multiReward(nb, steps-1, discount)
  return totalReward/len(ds)

def reinforce(board):
  ds = board.moveable()
  direction = ""
  maxReward = -board.capacity*100
  for d in ds:
    t = board.moveTarget(d)
    nb = board.move("",t)
    r = reward(board, t) + multiReward(nb, 5, 0.8)
    if r > maxReward:
      maxReward = r
      direction = d
  rat = 0.8
  #if maxReward < 0:
  #  rat = 0.5
  if (np.random.random() < rat):
    return direction
  return ds[int(np.random.random()*len(ds))]

def goThrough(r,c,path):
  b = Board(r,c)
  b.restore(np.array([[2,0,4],[8,7,5],[1,3,6]]),np.array([0,1]))
  orig = b.currentBoard.copy()
  round = 0
  open("window.txt","w").write("Ready to start...")
  time.sleep(2)
  for p in path:
    round += 1
    print("Move:",p,reward(b,b.moveTarget(p)))
    b.move(p, b.defaultLoc)
    #print(b.currentBoard)
    f = open("window.txt", "w")
    f.write(str(b.currentBoard)+"\n\n"+"Move: "+p+"\n"+str(round))
    f.close()
    time.sleep(0.75)
  if b.bingo():
    print("恭喜你成功复原!")
    print("总步数：",round)
    print("起始：\n",orig)
    print("最终：\n",b.currentBoard)
  else:
    print("总步数：",round)
    print("超过步数限制")


# automatic(3,3, reinforce, 10000)
# play(3,3)
goThrough(3,3,"awwdsdadwassdwwsswaawswdswdaadaswdadadsdawdsswsaawdsdwwaa")
