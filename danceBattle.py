def markMoveAsDone( boolTable, moveList ):
	i = moveList[0]
	j = moveList[1]

	boolTable[i][j] = True
	boolTable[j][i] = True

file = open("danceTestCase1.txt", "r")

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

emptyRow = [ False for x in range(0,n) ]

for i in range(0,n):
	usedMoves.append([ False for x in range(0,n) ])

for move in inputMoves:
	markMoveAsDone( usedMoves, move )

print(usedMoves)
