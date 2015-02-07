
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

	def __init__( self, n, m, inputTurns ):
		self.n = n
		self.m = m
		self.inputTurns = inputTurns

		#Set up array of bools
		usedTurns = []

		for i in range(0,n):
			usedTurns.append([ False for x in range(0,n) ])

		for turn in self.inputTurns:
			markMoveAsDone( usedTurns, turn )

		#print2DArray(usedTurns)

		numInputTurns = len(self.inputTurns)

		isMyTurn = numInputTurns % 2 == 1

		self.lastTurn = inputTurns[numInputTurns - 1]

		self.initialState = danceState(isMyTurn, self.lastTurn, usedTurns)

class danceState:

	def __init__( self, isMyTurn, turn, usedTurns ):
		self.isMyTurn = isMyTurn # Identifying the person who performed the move to get here
		self.turn = turn
		self.prevMove = turn[1] # The last move in the turn used to get to this state
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

		childUsedTurns = deepcopy(self.data.usedTurns)

		childTurn = [ self.data.prevMove, moveNumber ]

		markMoveAsDone( childUsedTurns, childTurn )

		childNode = node( danceState( not self.data.isMyTurn, childTurn, childUsedTurns ), self )

		self.children.append( childNode )

		return childNode

	def evaluate(self):

		if len(self.children) == 0: # leaf node

			self.childChosen = None

			if self.data.isMyTurn:
				return 1 # I win
			else:
				return -1 # min wins

		else: # not leaf node

			if not self.data.isMyTurn:
				# look for max

				maxValue = None
				self.childChosen = None

				for childNode in self.children:
					value = childNode.evaluate()

					if maxValue is None or value > maxValue:
						maxValue = value
						#print("choosing node", childNode.data.turn)
						self.childChosen = childNode

				return maxValue

			else:
				# look for min

				minValue = None
				self.childChosen = None

				for childNode in self.children:
					value = childNode.evaluate()

					if minValue is None or value < minValue:
						minValue = value
						#print("choosing node", childNode.data.turn)
						self.childChosen = childNode

				return minValue


def readInProblem( fileName ):
	file = open( fileName, "r")

	#print(file.read())

	n = int(file.readline())
	m = int(file.readline())

	#print("N = {0} M = {1}".format(n,m))

	inputTurns = []

	for inputLineIndex in range(0, m):

		line = file.readline();
		line = line.replace('\n','')

		turn = line.split(' ')

		turn[0] = int(turn[0])
		turn[1] = int(turn[1])

		inputTurns.append(turn)

	file.close()

	return problem( n, m, inputTurns )

testCaseNum = input("Enter a test case number:\n")

problemObj = readInProblem("danceTestCase" + testCaseNum + ".txt")

rootNode = node( problemObj.initialState, None )

#print("expanding nodes")

rootNode.expand()

#print("evaluating nodes")

evaluation = rootNode.evaluate()

isMax = True

for turn in problemObj.inputTurns:
	if (isMax):
		print("Max:",turn)
	else:
		print("Min:",turn)
	isMax = not isMax

tempNode = rootNode
tempNode = tempNode.childChosen

while tempNode is not None:
	
	if (isMax):
		print("Max:",tempNode.data.turn)
	else:
		print("Min:",tempNode.data.turn)

	isMax = not isMax

	tempNode = tempNode.childChosen

if evaluation == 1:
	print("Win")
else:
	print("Lose")