
from copy import deepcopy

def markMoveAsDone( boolTable, moveList ):
	i = moveList[0]
	j = moveList[1]

	boolTable[i][j] = True
	boolTable[j][i] = True

def print2DArray( array ):
	for row in array:
		print(row)

# class for organizing the data about the problem
class problem:

	def __init__( self, n, m, initialState ):
		self.n = n
		self.m = m
		self.initialState = initialState

class danceState:

	def __init__( self, isMyTurn, prevMove, usedTurns ):
		self.isMyTurn = isMyTurn # Identifying the person who performed the move to get here
		self.prevMove = prevMove # The last move in the turn used to get to this state
		self.usedTurns = usedTurns

class node:
	
	def __init__(self, data, parent):
		self.data = data # danceState
		self.parent = parent
		self.children = []

	def expand(self):

		#print("trying to expand node")

		for moveNumber in range(0,len(self.data.usedTurns)):
			if self.data.usedTurns[self.data.prevMove][moveNumber] == False: # move has not been used

				childNode = self.createChildFromMove( moveNumber )

				childNode.expand()

		#print("node expanded")

	def createChildFromMove(self, moveNumber):

		childNode = node( deepcopy(self.data), self )

		childNode.data.isMyTurn = not self.data.isMyTurn
		childNode.data.prevMove = moveNumber
		markMoveAsDone( childNode.data.usedTurns, [ self.data.prevMove, moveNumber ] )
		self.children.append( childNode )

		return childNode

	def evaluate(self):

		if len(self.children) == 0: # leaf node
			if self.data.isMyTurn:
				return 1 # I win
			else:
				return -1 # min wins

		else: # not leaf node

			leafValues = []

			for childNode in self.children:
				leafValues.append( childNode.evaluate() )

			if not self.data.isMyTurn:
				# look for max

				maxValue = None

				for value in leafValues:
					if maxValue == None or value > maxValue:
						maxValue = value

				return maxValue

			else:
				# look for min

				minValue = None

				for value in leafValues:
					if minValue == None or value < minValue:
						minValue = value

				return minValue


def readInProblem( fileName ):
	file = open( fileName, "r")

	#print(file.read())

	n = int(file.readline())
	m = int(file.readline())

	#print("N = {0} M = {1}".format(n,m))

	inputMoves = []

	for inputLineIndex in range(0, m):

		line = file.readline();
		line = line.replace('\n','')

		move = line.split(' ')

		move[0] = int(move[0])
		move[1] = int(move[1])

		inputMoves.append(move)

	#print(inputMoves)

	#Set up array of bools
	usedTurns = []

	for i in range(0,n):
		usedTurns.append([ False for x in range(0,n) ])

	for move in inputMoves:
		markMoveAsDone( usedTurns, move )

	#print2DArray(usedTurns)

	numInputMoves = len(inputMoves)

	isMyTurn = numInputMoves % 2 == 1

	lastMove = inputMoves[numInputMoves - 1][1]

	file.close()

	return problem( n, m, danceState(isMyTurn, lastMove, usedTurns) )

testCaseNum = input("Enter a test case number:\n")

problemObj = readInProblem("danceTestCase" + testCaseNum + ".txt")

rootNode = node( problemObj.initialState, None )

print("expanding nodes")

rootNode.expand()

print("evaluating nodes")

evaluation = rootNode.evaluate()

if evaluation == 1:
	print("Win")
else:
	print("Lose")