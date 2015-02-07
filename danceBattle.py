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
		self.isMyTurn = isMyTurn
		self.prevMove = prevMove # The last move in the turn used to get to this state
		self.usedTurns = usedTurns

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

	isMyTurn = numInputMoves % 2 == 0

	lastMove = inputMoves[numInputMoves - 1][1]

	file.close()

	return problem( n, m, danceState(isMyTurn, lastMove, usedTurns) )

problemObj = readInProblem("danceTestCase1.txt")

print2DArray(problemObj.initialState.usedTurns)