#! /usr/bin/env python

import os, random, select, sys, termios, time, tty

# Flow control variables
timepool=0
previoustime=time.time()
# Other variables
lastpressed=""
points=0

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
    self.heads=1
    self.child=None
    self.movedir=""

  def split(self):
    """
    Adds a second head to the snake
    """

    self.heads=2
    if self.movedir in ["left", "right"]:
      self.child=snake(self.body[0][0],self.body[0][1]+1)
      self.child.movedir="up"
    else: 
      self.child=snake(self.body[0][0]+1,self.body[0][1])
      self.child.movedir="left"

  def merge(self):
    """
    Joins two snakes together
    """

    global points

    if self.child.body[0]==self.trail:
      self.heads=1
      self.trail=self.child.trail
      self.body+=self.child.body
      self.child=None
      return 1
      points+=10

    if self.body[0]==self.child.trail:
      self.heads=1
      self.body=self.child.body+self.body
      self.child=None
      return 1
      points+=10

    return 0

  def gonnadie(self,arena):
    """
    Receives a map

    Returns 1 if there is an obstacle in the way
    """

    if self.movedir==None: return -1

    if self.movedir=="up" : 
      if arena.space[self.body[0][1]-1][self.body[0][0]] in ["A", "O"] or self.body[0][1]-1<0 :
        return 1 
      elif arena.space[self.body[0][1]-1][self.body[0][0]]=="8":
        return 2
      return 0
    if self.movedir=="down" : 
      if arena.space[self.body[0][1]+1][self.body[0][0]] in ["A", "O"] or self.body[0][1]+1>39:
        return 1 
      elif arena.space[self.body[0][1]+1][self.body[0][0]]=="8":
        return 2
      return  0
    if self.movedir=="left" : 
      if arena.space[self.body[0][1]][self.body[0][0]-1] in ["A", "O"] or self.body[0][0]-1<0 :
        return 1 
      elif arena.space[self.body[0][1]][self.body[0][0]-1]=="8":
        return 2
      return 0
    if self.movedir=="right": 
      if arena.space[self.body[0][1]][self.body[0][0]+1] in ["A", "O"] or self.body[0][0]+1>39:
        return 1 
      elif arena.space[self.body[0][1]][self.body[0][0]+1]=="8":
        return 2
      return  0
    return 0

  def move(self,arena):
    """
    Moves in a movedir
    """

    global points

    if self.movedir==None: return -1
    deadsoon=self.gonnadie(arena)
    if deadsoon!=1 and self.movedir:
      if   self.movedir=="up"    : nextpos=[[self.body[0][0]   ,self.body[0][1]-1]]
      elif self.movedir=="down"  : nextpos=[[self.body[0][0]   ,self.body[0][1]+1]]
      elif self.movedir=="left"  : nextpos=[[self.body[0][0]-1 ,self.body[0][1]  ]]
      elif self.movedir=="right" : nextpos=[[self.body[0][0]+1 ,self.body[0][1]  ]]
      self.trail=self.body[-1]
      self.body=nextpos+self.body

      # End the game if not in merging condiitions
      if deadsoon==1: gameover()
      # No problemo
      if deadsoon!=2:
        self.body=self.body[:-1]
      # There is food
      if deadsoon==2:
        points+=5
        while 1:
          randomx=random.randrange(40)
          randomy=random.randrange(20)
          if arena.space[randomy][randomx]==".": arena.space[randomy][randomx]="8";break
      return 1
    return -1

#Auxiliiar functions
def draw(arena,player):
  """
  Draws the game field from the arena and player data

  Also prints a line with info
  """

  drawmat=arena.space
  for i in player.body:
    drawmat[i[1]][i[0]]="O"
  for i in drawmat:
    print "".join(i)
  drawmat[player.trail[1]][player.trail[0]]="."
  if player.heads==2:
    for i in player.child.body:
      drawmat[i[1]][i[0]]="O"
    drawmat[player.child.trail[1]][player.child.trail[0]]="."

  
  print points,"points"

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

  timepool=0 if timepool*1000>=300 else timepool+time.time()-previoustime
  previoustime=time.time()
  return not timepool

def pressed():
  """
  Returns a pressed key (Supposedly non-blocking)
  """

  def isData():
    return select.select([sys.stdin], [], [], 0.01)==([sys.stdin], [], [])

  c=""
  old_settings=termios.tcgetattr(sys.stdin)
  try:
    tty.setcbreak(sys.stdin.fileno())
    if isData():
      c=sys.stdin.read(1)
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return c

def gameover():
  """
  Displays a game over message
  """

  raw_input("gameover")
  exit()

def mainloop(arena,player):
  """
  Main game loop
  """

  global lastpressed
  global points
  previouspressed=lastpressed
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
  elif cyclekey=="q": os.system('tput clear'); exit()


  if loopmanage():

    os.system('tput clear')
    if player.heads==1:
      if player.movedir: points+=1
      if lastpressed[:-1] in ["up", "down", "left", "right"]:
        player.movedir=lastpressed[:-1]
      elif lastpressed=="split": 
        player.split()
        player.child.move(arena)
      player.move(arena)
    else:
      points+=2
      if lastpressed[-1]=="1":    player.movedir=lastpressed[:-1]
      elif lastpressed[-1]=="2":  player.child.movedir=lastpressed[:-1]
      player.move(arena)
      player.child.move(arena)
      if player.trail==player.child.body[0] or player.body[0]==player.child.trail:
        player.merge()
    draw(arena,player)

# Launch code
if __name__=="__main__":
  
  arena,player=newgame()
  os.system('tput clear')
  draw(arena,player)
  while 1:
    mainloop(arena,player)
