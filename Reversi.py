import turtle
import math
import time

#Switches the color being played (mimics the switching of a move)
#Affects global variables
def colorSwitch():
  global color
  global colorName
  if (color==1):
    color=0
    colorName='White'
  else:
    color=1
    colorName='Black'

#Places a disc on the board at a certain column and row and with a certain color
#Throughout the program, 0 indicates white, 1 indicates black, and -5 indicates empty
def placeDiscColor(column,row,color):
  global currentBoard

  #Gets the turtle to the position chosen
  turtle.penup()
  turtle.setpos((column-4)*60-30,(4-row)*60+10)
  turtle.pendown()

  #Makes the disc (colored in if black)
  if (color==1):
    turtle.begin_fill()
    turtle.circle(20)
    turtle.end_fill()
  else:
    turtle.circle(20)

  #Updates the matrix that is keeping track of the game board
  currentBoard[row-1][column-1]=color

#Changes the color of a disc at a certain position
def flipColor(column,row):
  global currentBoard
  #Places a large white circle over the existing disc, effectively clearing anything that was there
  turtle.penup()
  turtle.pencolor('#FFFFFF')
  turtle.setpos((column-4)*60-30,(4-row)*60+9)
  turtle.pendown()
  turtle.fillcolor('#FFFFFF')
  turtle.begin_fill()
  turtle.circle(22)
  turtle.end_fill()

  #Resets the colors for turtle
  turtle.fillcolor('#000000')
  turtle.pencolor('#000000')

  #Switches the value of the color in the matrix
  if(currentBoard[row-1][column-1]==0):
    currentBoard[row-1][column-1]=1
  else:
    currentBoard[row-1][column-1]=0

  #Places a new disc in place of the old disc, this time of the opposite color
  placeDiscColor(column,row,currentBoard[row-1][column-1])

#Checks to see if a move is valid or not. Returns True or False
#Need this for the 1-player version of the game as the computer needs to know whether it is making a valid move
#Also needed for end-game analysis. Need to be able to determine if a player has a valid move or not. If no valid moves for both players, then the game is over. If no valid moves for one player, their move is skipped.
def isValidMove(column,row):
  global color
  global currentBoard
  colCounter=0
  rowCounter=0

  #Need to be choosing an empty position on the board at which to place the disc
  if (currentBoard[row-1][column-1]==-5):

    #Need to check if the move is valid in 8 directions
    #Checks top left
    #Want to make sure there is a square in that direction of the chosen square
    if (column>1 and row>1):

      #Checking to see if the disc (if any) in that direction is of opposite color as the played disc
      if (abs(currentBoard[row-2][column-2]-color)==1):
        colCounter=3
        rowCounter=3

        #Continuing in that direction
        while ((column-colCounter)>=0 and (row-rowCounter)>=0):

          #Case 1: If the next square has a disc that is the same color as the played disc, the move is valid
          if (abs(currentBoard[row-rowCounter][column-colCounter]-color)==0):
            return True

          #Case 2: If the next square is empty, this direction does not work
          elif (abs(currentBoard[row-rowCounter][column-colCounter]-color)!=1):
            break

          #Case 3: If the next square has a disc that is of opposite color as the played disc, keep checking the same direction
          else:
            colCounter+=1
            rowCounter+=1

    #checks left
    if (column>1):
      if (abs(currentBoard[row-1][column-2]-color)==1):
        colCounter=3
        while ((column-colCounter)>=0):
          if (abs(currentBoard[row-1][column-colCounter]-color)==0):
            return True
          elif (abs(currentBoard[row-1][column-colCounter]-color)!=1):
            break
          else:
            colCounter+=1

    #checks bottom left
    if (column>1 and row<8):
      if (abs(currentBoard[row][column-2]-color)==1):
        colCounter=3
        rowCounter=1
        while ((column-colCounter)>=0 and (row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column-colCounter]-color)==0):
            return True
          elif (abs(currentBoard[row+rowCounter][column-colCounter]-color)!=1):
            break
          else:
            colCounter+=1
            rowCounter+=1

    #checks down
    if (row<8):
      if (abs(currentBoard[row][column-1]-color)==1):
        rowCounter=1
        while ((row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column-1]-color)==0):
            return True
          elif (abs(currentBoard[row+rowCounter][column-1]-color)!=1):
            break
          else:
            rowCounter+=1

    #checks up
    if (row>1):
      if (abs(currentBoard[row-2][column-1]-color)==1):
        rowCounter=3
        while ((row-rowCounter)>=0):
          if (abs(currentBoard[row-rowCounter][column-1]-color)==0):
            return True
          elif (abs(currentBoard[row-rowCounter][column-1]-color)!=1):
            break
          else:
            rowCounter+=1

    #checks top right
    if (column<8 and row>1):
      if (abs(currentBoard[row-2][column]-color)==1):
        colCounter=1
        rowCounter=3
        while ((column+colCounter)<=7 and (row-rowCounter)>=0):
          if (abs(currentBoard[row-rowCounter][column+colCounter]-color)==0):
            return True
          elif (abs(currentBoard[row-rowCounter][column+colCounter]-color)!=1):
            break
          else:
            colCounter+=1
            rowCounter+=1

    #checks right
    if (column<8):
      if (abs(currentBoard[row-1][column]-color)==1):
        colCounter=1
        while ((column+colCounter)<=7):
          if (abs(currentBoard[row-1][column+colCounter]-color)==0):
            return True
          elif (abs(currentBoard[row-1][column+colCounter]-color)!=1):
            break
          else:
            colCounter+=1

    #checks bottom right
    if (column<8 and row<8):
      if (abs(currentBoard[row][column]-color)==1):
        colCounter=1
        rowCounter=1
        while ((column+colCounter)<=7 and (row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column+colCounter]-color)==0):
            return True
          elif (abs(currentBoard[row+rowCounter][column+colCounter]-color)!=1):
            break
          else:
            colCounter+=1
            rowCounter+=1
  return False

#Counts how many discs of the opposite will be flipped if the position inputted is chosen
#Used for 1-player to help the computer make the best possible move (without regards to the overall game or strategy, but rather in regards to the optimal move at that instant)
def makeMoveCounter(column,row):
  global color
  global currentBoard
  colCounter=0
  rowCounter=0
  returnCounter=0
  if (currentBoard[row-1][column-1]==-5):

    #Once again, must check all 8 directions and add the total number of discs flipped for all 8 directions given the chosen position
    #Checks top left
    colCounter=2
    rowCounter=2

    #Counts how many discs will be flipped in this direction, knowing that the path is valid
    while ((column-colCounter)>=0 and (row-rowCounter)>=0):

      #While traveling in this direction, if the color of the disc on the board differs from the color of the disc played, the number of discs that will be flipped increases by 1
      if (abs(currentBoard[row-rowCounter][column-colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
        rowCounter+=1
      else:
        break

    #checks left
    colCounter=2
    while ((column-colCounter)>=0):
      if (abs(currentBoard[row-1][column-colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
      else:
        break

    #checks bottom left
    colCounter=2
    rowCounter=0
    while ((column-colCounter)>=0 and (row+rowCounter)<=7):
      if (abs(currentBoard[row+rowCounter][column-colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
        rowCounter+=1
      else:
        break

    #checks down
    rowCounter=0
    while ((row+rowCounter)<=7):
      if (abs(currentBoard[row+rowCounter][column-1]-color)==1):
        returnCounter+=1
        rowCounter+=1
      else:
        break

    #checks up
    rowCounter=2
    while ((row-rowCounter)>=0):
      if (abs(currentBoard[row-rowCounter][column-1]-color)==1):
        returnCounter+=1
        rowCounter+=1
      else:
        break

    #checks top right
    colCounter=0
    rowCounter=2
    while ((column+colCounter)<=7 and (row-rowCounter)>=0):
      if (abs(currentBoard[row-rowCounter][column+colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
        rowCounter+=1
      else:
        break

    #checks right
    colCounter=0
    while ((column+colCounter)<=7):
      if (abs(currentBoard[row-1][column+colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
      else:
        break

    #checks bottom right
    colCounter=0
    rowCounter=0
    while ((column+colCounter)<=7 and (row+rowCounter)<=7):
      if (abs(currentBoard[row+rowCounter][column+colCounter]-color)==1):
        returnCounter+=1
        colCounter+=1
        rowCounter+=1
      else:
        break
  return returnCounter

#For user-inputted moves, this function checks all 8 paths to see if the direction is valid, flips the colors of opposite-colored, sandwiched discs, and places the disc on the chosen position
def makeMove(column,row):
  global color
  global currentBoard
  colCounter=0
  rowCounter=0
  pathWorks = False
  time.sleep(1.5)
  placeDiscColor(column,row,color)
  if (currentBoard[row-1][column-1]==1 or currentBoard[row-1][column-1]==0):

    #Once again, must check all 8 directions and flip sandwiched discs for all 8 directions given the chosen position
    #checks top left
    if (column>1 and row>1):
      if (abs(currentBoard[row-2][column-2]-color)==1):
        colCounter=3
        rowCounter=3
        while ((column-colCounter)>=0 and (row-rowCounter)>=0):
          if (abs(currentBoard[row-rowCounter][column-colCounter]-color)==0):
            pathWorks=True
            colCounter=column + 1
          elif (abs(currentBoard[row-rowCounter][column-colCounter]-color)!=1):
            colCounter=column + 1
          else:
            colCounter+=1
            rowCounter+=1

      #If this path works, flip the colors of all discs in that direction that are of opposite color until you hit a disc of the same color
      if (pathWorks):
        colCounter=2
        rowCounter=2
        while ((column-colCounter)>=0 and (row-rowCounter)>=0 and pathWorks):
          if (abs(currentBoard[row-rowCounter][column-colCounter]-color)==1):
            flipColor(column-colCounter+1,row-rowCounter+1)
            colCounter+=1
            rowCounter+=1
          else:
            pathWorks=False

    #checks left
    if (column>1):
      if (abs(currentBoard[row-1][column-2]-color)==1):
        colCounter=3
        while ((column-colCounter)>=0):
          if (abs(currentBoard[row-1][column-colCounter]-color)==0):
            pathWorks=True
            colCounter=column + 1
          elif (abs(currentBoard[row-1][column-colCounter]-color)!=1):
            colCounter=column + 1
          else:
            colCounter+=1
      if (pathWorks):
        colCounter=2
        while ((column-colCounter)>=0 and pathWorks):
          if (abs(currentBoard[row-1][column-colCounter]-color)==1):
            flipColor(column-colCounter+1,row)
            colCounter+=1
          else:
            pathWorks=False

    #checks bottom left
    if (column>1 and row<8):
      if (abs(currentBoard[row][column-2]-color)==1):
        colCounter=3
        rowCounter=1
        while ((column-colCounter)>=0 and (row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column-colCounter]-color)==0):
            pathWorks=True
            colCounter=column + 1
          elif (abs(currentBoard[row+rowCounter][column-colCounter]-color)!=1):
            colCounter=column + 1
          else:
            colCounter+=1
            rowCounter+=1
      if (pathWorks):
        colCounter=2
        rowCounter=0
        while ((column-colCounter)>=0 and (row+rowCounter)<=7 and pathWorks):
          if (abs(currentBoard[row+rowCounter][column-colCounter]-color)==1):
            flipColor(column-colCounter+1,row+rowCounter+1)
            colCounter+=1
            rowCounter+=1
          else:
            pathWorks=False

    #checks down
    if (row<8):
      if (abs(currentBoard[row][column-1]-color)==1):
        rowCounter=1
        while ((row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column-1]-color)==0):
            pathWorks=True
            rowCounter=8
          elif (abs(currentBoard[row+rowCounter][column-1]-color)!=1):
            rowCounter=8
          else:
            rowCounter+=1
      if (pathWorks):
        rowCounter=0
        while ((row+rowCounter)<=7 and pathWorks):
          if (abs(currentBoard[row+rowCounter][column-1]-color)==1):
            flipColor(column,row+rowCounter+1)
            rowCounter+=1
          else:
            pathWorks=False

    #checks up
    if (row>1):
      if (abs(currentBoard[row-2][column-1]-color)==1):
        rowCounter=3
        while ((row-rowCounter)>=0):
          if (abs(currentBoard[row-rowCounter][column-1]-color)==0):
            pathWorks=True
            rowCounter=row+1
          elif (abs(currentBoard[row-rowCounter][column-1]-color)!=1):
            rowCounter=row+1
          else:
            rowCounter+=1
      if (pathWorks):
        rowCounter=2
        while ((row-rowCounter)>=0 and pathWorks):
          if (abs(currentBoard[row-rowCounter][column-1]-color)==1):
            flipColor(column,row-rowCounter+1)
            rowCounter+=1
          else:
            pathWorks=False

    #checks top right
    if (column<8 and row>1):
      if (abs(currentBoard[row-2][column]-color)==1):
        colCounter=1
        rowCounter=3
        while ((column+colCounter)<=7 and (row-rowCounter)>=0):
          if (abs(currentBoard[row-rowCounter][column+colCounter]-color)==0):
            pathWorks=True
            colCounter=8
          elif (abs(currentBoard[row-rowCounter][column+colCounter]-color)!=1):
            colCounter=8
          else:
            colCounter+=1
            rowCounter+=1
      if (pathWorks):
        colCounter=0
        rowCounter=2
        while ((column+colCounter)<=7 and (row-rowCounter)>=0 and pathWorks):
          if (abs(currentBoard[row-rowCounter][column+colCounter]-color)==1):
            flipColor(column+colCounter+1,row-rowCounter+1)
            colCounter+=1
            rowCounter+=1
          else:
            pathWorks=False

    #checks right
    if (column<8):
      if (abs(currentBoard[row-1][column]-color)==1):
        colCounter=1
        while ((column+colCounter)<=7):
          if (abs(currentBoard[row-1][column+colCounter]-color)==0):
            pathWorks=True
            colCounter=8
          elif (abs(currentBoard[row-1][column+colCounter]-color)!=1):
            colCounter=8
          else:
            colCounter+=1
      if (pathWorks):
        colCounter=0
        while ((column+colCounter)<=7 and pathWorks):
          if (abs(currentBoard[row-1][column+colCounter]-color)==1):
            flipColor(column+colCounter+1,row)
            colCounter+=1
          else:
            pathWorks=False

    #Checks bottom right
    if (column<8 and row<8):
      if (abs(currentBoard[row][column]-color)==1):
        colCounter=1
        rowCounter=1
        while ((column+colCounter)<=7 and (row+rowCounter)<=7):
          if (abs(currentBoard[row+rowCounter][column+colCounter]-color)==0):
            pathWorks=True
            colCounter=8
          elif (abs(currentBoard[row+rowCounter][column+colCounter]-color)!=1):
            colCounter=8
          else:
            colCounter+=1
            rowCounter+=1
      if (pathWorks):
        colCounter=0
        rowCounter=0
        while ((column+colCounter)<=7 and (row+rowCounter)<=7 and pathWorks):
          if (abs(currentBoard[row+rowCounter][column+colCounter]-color)==1):
            flipColor(column+colCounter+1,row+rowCounter+1)
            colCounter+=1
            rowCounter+=1
          else:
            pathWorks=False
  colorSwitch()

#Allows the user to input the column and row they want to put the disc at.
#Returns a tuple to be able to return both the column and the row chosen
def getColRow():
  global colorName
  column=input('\nDisc\'s column for ' + colorName + ': ')
  while (not(column.isnumeric() and (int(column) in range(1,9)))):
    column=input('Not valid column. Let\'s try again. Disc\'s column: ')
  row=input('Disc\'s row for ' + colorName + ': ')
  while (not(row.isnumeric() and (int(row) in range(1,9)))):
    row=input('Not valid row. Let\'s try again. Disc\'s row: ')
  column=int(column)
  row=int(row)
  return(column,row)

#Once the game ends, the user is given the option to play again
def playAgain():
  playAgainYN = 0
  playAgainYN = input('\nDo you want to play again? Type 1 for yes and 2 for no. ')
  while (not(playAgainYN.isnumeric() and (int(playAgainYN)==1 or int(playAgainYN)==2))):
    playAgainYN=input('\nLet\'s try again. Do you want to play again? Type 1 for yes and 2 for no.  ')
  if (int(playAgainYN)==1):
    turtle.reset()
    startGame()
  else:
    print('Thank you for playing!')

#Once the game has officially ended, this function figures out the winner
def endGame():
  global currentBoard
  whiteCounter=0
  blackCounter=0
  for i in range(0,8):
    for j in range(0,8):
      if (currentBoard[i][j]==0):
        whiteCounter+=1
      elif (currentBoard[i][j]==1):
        blackCounter+=1
  if (whiteCounter>blackCounter):
    print('White wins! Congratulations!')
  elif (blackCounter>whiteCounter):
    print('Black wins! Congratulations!')
  else:
    print('It was a tie!')
  playAgain()

#Keeps the game recursing, allowing for multiple moves to happen and checking to see if the player has a valid move to play their disc
def keepPlaying():
  global colorName
  global color
  global gameType
  global gameEndingCheck
  validMoveExists = False

  #Checks every square on the board to see if that square is a valid move for the player
  for i in range(1,9):
    for j in range(1,9):
      if isValidMove(i,j):
        validMoveExists = True
        break
    if validMoveExists:
      break

  #If there theoretically is a valid move, continue to play the game
  if validMoveExists:
    if (gameType==1):
      getMove1()
    else:
      getMove2()

  #If there is no valid move for this color, switch the colors and keep playing.
  else:
    print('No valid move exists for '+colorName+'.')
    gameEndingCheck+=1

    #If both players have no valid moves, end the game
    if (gameEndingCheck==2):
      endGame()
    else:
      colorSwitch()
      print('It is now '+colorName+'\'s turn.')
      keepPlaying()

#Chooses and plays the computer's best move based on most coins taken
def findBestMove():
  global colorName
  time.sleep(1)
  count=0
  column=0
  row=0
  #Checks every square and figures out how many discs will be flipped if that square is played. Chooses the square with the most coins flipped
  for i in range(1,9):
    for j in range(1,9):
      if isValidMove(i,j):
        countTemp=makeMoveCounter(i,j)
        if(countTemp>count):
          count=countTemp
          column=i
          row=j
  print('\n'+colorName+' will play the move Column: '+str(column)+' Row: '+str(row))
  makeMove(column,row)

#Makes a move for a one-player game
#For the variable move, 0 means user to play and 1 means computer to play
def getMove1():
  global gameEndingCheck
  global move
  gameEndingCheck=0

  #User plays a move
  if (move==0):
    answerTuple=getColRow()
    column=answerTuple[0]
    row=answerTuple[1]
    while (not isValidMove(column,row)):
      print('Sorry! That\'s not a valid move. Please try again.')
      answerTuple=getColRow()
      column=answerTuple[0]
      row=answerTuple[1]
    makeMove(column,row)

  #Computer plays a move
  else:
    findBestMove()

  #The turn keeps switching
  if (move==0):
    move=1
  else:
    move=0
  keepPlaying()

#Makes moves for two-player games
def getMove2():
  global gameEndingCheck
  gameEndingCheck=0
  answerTuple=getColRow()
  column=answerTuple[0]
  row=answerTuple[1]
  while (not isValidMove(column,row)):
    print('Sorry! That\'s not a valid move. Please try again.')
    answerTuple=getColRow()
    column=answerTuple[0]
    row=answerTuple[1]
  makeMove(column,row)
  keepPlaying()

#Sets up the board
def setUpBoard():
  global gameType

  #Sets up the 8-by-8 grid for the game board
  turtle.hideturtle()
  turtle.speed(100)
  turtle.pensize(1)
  squareSize=60
  gridSize=8
  for i in range(-gridSize//2, int(math.ceil(gridSize/2))+1):
    turtle.penup()
    turtle.setpos(-gridSize*squareSize/2, i*squareSize)
    turtle.pendown()
    turtle.setpos(gridSize*squareSize/2, i*squareSize)
  for j in range(-gridSize//2, int(math.ceil(gridSize/2))+1):
    turtle.penup()
    turtle.setpos(j*squareSize, -gridSize*squareSize/2)
    turtle.pendown()
    turtle.setpos(j*squareSize, gridSize*squareSize/2)

  #Places the initial 4 discs on the board
  placeDiscColor(4,4,0)
  placeDiscColor(4,5,1)
  placeDiscColor(5,5,0)
  placeDiscColor(5,4,1)
  if (gameType==1):
    getMove1()
  else:
    getMove2()

#Starts the game and determines the game format (1-player or 2-player)
def startGame():
  global gameType
  print('Hello! Welcome to Reversi! The point of the game is to have the most discs of your color as possible.')
  print('\nWhen you make a move, start from the top left and count the number of columns across you want the disc to be played. Enter this number first. Then, when prompted again, choose the row. The first column is 1, second is 2, and so forth. The same pattern holds true for rows.')
  gameType=input('\nDo you want to play 1 player (type the digit 1) or 2 player (type the digit 2)? ')
  while (not(gameType.isnumeric() and (int(gameType)==1 or int(gameType)==2))):
    gameType=input('\nLet\'s try again. Do you want to play 1 player (type the digit 1) or 2 player (type the digit 2)? ')
  gameType=int(gameType)
  setUpBoard()

#Global variables
move=0
color=0
gameEndingCheck=0
colorName='White'
gameType=0
currentBoard=[[-5 for x in range(8)] for y in range(8)]

startGame()
