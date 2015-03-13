
import string
from random import random

boysFileName = "namesBoys.txt"
girlsFileName = "namesGirls.txt"

startCharacter = '<'
endCharacter = '>'

allCharacters = startCharacter + string.ascii_lowercase + endCharacter

file = open( boysFileName, "r")

nameList = []

# add an entry to a dictionary for all valid characters
def addEntryForAllCharacters( dictionary ):
	for char in allCharacters:
		dictionary[ char ] = {}

def setZeroForAllCharacters( dictionary ):
	for char in allCharacters:
		dictionary[ char ] = 0

for line in file:

	line = line.replace("\n","")

	line = ( startCharacter + line + endCharacter ).lower()

	nameList.append( line )

file.close()

frequencyData = {}

# set up frequency data dictionary
addEntryForAllCharacters( frequencyData )

for char in allCharacters:
	setZeroForAllCharacters( frequencyData[ char ] )

for name in nameList:
	for charIndex in range( 0, len( name ) - 1 ):

		char = name[ charIndex ]

		nextChar = name[ charIndex + 1 ]

		if ( not char == endCharacter ):

			# add 1 to the frequency table

			frequencyData[ char ][ nextChar ] += 1

#print( frequencyData )

# normalize data

normalizedData = {}

# set up normalized data
addEntryForAllCharacters( normalizedData )

for char in allCharacters:
	setZeroForAllCharacters( normalizedData[ char ] )

for char in allCharacters:

	row = frequencyData[ char ]

	sum = 0

	for nextChar in allCharacters:
		sum += row[ nextChar ]
	
	#print( char + " " + str( sum ) )

	if ( not sum == 0 ):
		for nextChar in allCharacters:

			#print( str( row[ nextChar ] ) + " / " + str( sum ) + " = " + str( row[ nextChar ] / sum ) )

			normalizedData[ char ][ nextChar ] = float(row[ nextChar ]) / float(sum)

#print( frequencyData[ "<"] )
#print( normalizedData["<"] )

initialPrefix = startCharacter

generatedName = initialPrefix

currChar = startCharacter
nextChar = ""

while( True ):

	randVal = random()

	partialSum = 0

	for char in allCharacters:
		partialSum += normalizedData[ currChar ][ char ]
		if ( randVal < partialSum ):
			nextChar = char
			break

	if ( nextChar == endCharacter ):
		break

	generatedName += nextChar

	currChar = nextChar

generatedName = generatedName.replace( initialPrefix, "" )

print( generatedName )