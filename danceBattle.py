def markMoveAsDone( boolTable, moveList ):
	i = moveList[0]
	j = moveList[1]

	boolTable[i][j] = 1
	boolTable[j][i] = 1

def print2DArray( array ):
	for row in array:
		print(row)

# class for organizing the data about the problem
class problem:

	def __init__( self, n, m, isMyTurn, usedMoves ):
		self.n = n
		self.m = m
		self.isMyTurn = isMyTurn
		self.usedMoves = usedMoves


def readInProblem( fileName ):
	file = open( fileName, "r")

	#print(file.read())

	n = int(file.readline())
	m = int(file.readline())

	print("N = {0} M = {1}".format(n,m))

	inputMoves = []

	for inputLineIndex in range(0, m):

		line = file.readline();
		line = line.replace('\n','')

		move = line.split(' ')

		move[0] = int(move[0])
		move[1] = int(move[1])

		inputMoves.append(move)

	print(inputMoves)

	#Set up array of bools
	usedMoves = []

	for i in range(0,n):
		usedMoves.append([ 0 for x in range(0,n) ])

	for move in inputMoves:
		markMoveAsDone( usedMoves, move )

	print2DArray(usedMoves)

	isMyTurn = len(inputMoves) % 2 == 0

	file.close()

	return problem( n, m, isMyTurn, usedMoves)

problemObj = readInProblem("danceTestCase1.txt")

print(problemObj.isMyTurn)