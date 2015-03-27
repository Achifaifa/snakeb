#! /usr/bin/env python

import os, random, time

class sand:
  """
  Contains the campsite with obstacles and layout
  """

  def __init__(self,x,y):
    """
    Constructor. Creates a game zone of XxY squares

    recommended 40x20
    """

    sand.space=[["." for i in range(x)] for j in range(y)]
    for i in range(7):
      sand.space[random.randrange(y)][random.randrange(x)]="A"
    sand.space[random.randrange(y)][random.randrange(x)]="8"

class snake:
  """
  Main snake class
  """

  def __init__(self,x,y):
    """
    Initializes a snake in (x,y)
    """
    self.body=[[x,y]]
    self.trail=[x,y]

  def grow(self):
    """
    Adds the trail position to the snake
    """

    self.body.append(self.trail)

  def move(self,direction=None):
    """
    Moves in a direction
    """

    if direction==None:
      return 

    self.trail=self.body[-1]
    self.body=self.body[:-1]
    try:
      if direction=="up":     nextpos=[[self.body[0][0]-1,self.body[0][1]]]
      elif direction=="down":   nextpos=[[self.body[0][0]+1,self.body[0][1]]]
      elif direction=="left":   nextpos=[[self.body[0][0],self.body[0][1]-1]]
      elif direction=="right":  nextpos=[[self.body[0][0],self.body[0][1]+1]]
    except IndexError: 
      return
    self.body=nextpos+self.body

# Flow control variables
timepool=0
previoustime=time.time()

#Auxiliiar functions
def draw(arena,player):
  """
  Draws the game field from the arena and player data

  Also prints a line with info
  """

  drawmatrix=arena.space
  for i in player.body:
    drawmatrix[i[1]][i[0]]="O"
  for i in drawmatrix:
    print "".join(i)
  print timepool,time.time()

def newgame():
  """
  Creates a new game
  """

  arena=sand(40,20)
  while 1:
    tempx,tempy=random.randrange(40),random.randrange(20)
    if arena.space[tempy][tempx]==".": player=snake(tempx,tempy); break
  return arena,player

def loopmanage():
  """
  Internally manages the main game loop cycles 
  """

  global timepool
  global previoustime

  timepool+=(time.time()-previoustime)
  if timepool*1000>=50: timepool=0
  previoustime=time.time()
  return 1 if timepool==0 else 0

def mainloop(arena,player):
  """
  Main game loop
  """

  if loopmanage():
    os.system('clear')
    draw(arena,player)

# Launch code
if __name__=="__main__":
  
  arena,player=newgame()
  os.system('clear')
  draw(arena,player)
  while 1:
    mainloop(arena,player)