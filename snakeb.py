#! /usr/bin/env python

import os, random, select, sys, termios, time, tty

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
# Other variables
lastpressed=""

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
  print time.time()

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

  timepool=0 if timepool*1000>=50 else timepool+time.time()-previoustime
  previoustime=time.time()
  return not timepool

def pressed():
  """
  Returns a pressed key (Supposedly non-blocking)
  """

  def isData():
    return select.select([sys.stdin], [], [], 0.001)==([sys.stdin], [], [])

  c=""
  old_settings=termios.tcgetattr(sys.stdin)
  try:
    tty.setcbreak(sys.stdin.fileno())
    if isData():
      c=sys.stdin.read(1)
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return c

def mainloop(arena,player):
  """
  Main game loop
  """

  global lastpressed

  cyclekey=pressed()
  if   cyclekey=="w": lastpressed="up1"     # W in querty
  elif cyclekey=="a": lastpressed="left1"   # A in querty
  elif cyclekey=="r": lastpressed="down1"   # S in querty
  elif cyclekey=="s": lastpressed="right1"  # D in querty
  elif cyclekey=="u": lastpressed="up2"     # I in querty
  elif cyclekey=="n": lastpressed="left2"   # J in querty
  elif cyclekey=="e": lastpressed="down2"   # K in querty
  elif cyclekey=="i": lastpressed="right2"  # L in querty
  elif cyclekey==" ": lastpressed="split"
  elif cyclekey=="q": lastpressed="quit"


  if loopmanage():
    os.system('clear')
    draw(arena,player)
    print lastpressed

# Launch code
if __name__=="__main__":
  
  arena,player=newgame()
  os.system('clear')
  draw(arena,player)
  while 1:
    mainloop(arena,player)
  # while 1:
  #   print ispressed("a")