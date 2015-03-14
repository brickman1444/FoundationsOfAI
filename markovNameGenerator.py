
import string
from random import random

boysFileName = "namesBoys.txt"
girlsFileName = "namesGirls.txt"

startCharacter = '<'
endCharacter = '>'

allCharacters = startCharacter + string.ascii_lowercase + endCharacter

# add an entry to a dictionary for all valid characters
def addEntryForAllCharacters( dictionary ):
	for char in allCharacters:
		dictionary[ char ] = {}

def setZeroForAllCharacters( dictionary ):
	for char in allCharacters:
		dictionary[ char ] = 0

def readFileIntoList( fileName ):

	nameList = []

	file = open( fileName, "r" )

	for line in file:

		line = line.replace("\n","")

		line = ( startCharacter + line + endCharacter ).lower()

		nameList.append( line )

	file.close()

	return nameList

def getFrequencyData( nameList ):

	frequencyData = {}

	# set up frequency data dictionary
	addEntryForAllCharacters( frequencyData )

	for char in allCharacters:
		setZeroForAllCharacters( frequencyData[ char ] )

	for name in nameList:
		for charIndex in range( 0, len( name ) - 1 ):

			char = name[ charIndex ]

			if ( char == endCharacter ):
				break

			nextChar = name[ charIndex + 1 ]

			frequencyData[ char ][ nextChar ] += 1

	return frequencyData

def getNormalizedData( frequencyData ):
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

				normalizedData[ char ][ nextChar ] = float(row[ nextChar ]) / float(sum)

	return normalizedData

def generateName( normalizedData, nameList, minLength, maxLength ):

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

	nameLength = len( generatedName )

	if ( nameLength < minLength or nameLength > maxLength or generatedName in nameList):

		# Outside of range. Regenerate.
		return generateName( normalizedData, nameList, minLength, maxLength )
	else:
		return generatedName


'''
fileName = ""
while ( True ):
	genderChoice = input( "Male (m) or female (f)?" )
	if ( genderChoice == "m" ):
		fileName = boysFileName
		break
	elif ( genderChoice == "f" ):
		fileName = girlsFileName
		break

minLength = 0

while ( True ):
	minLength = int( input( "Minimum name length?" ) )

	if ( minLength > 0 ):
		break

maxLength = 0

while ( True ):
	maxLength = int( input( "Maximum name length?" ) )

	if ( maxLength >= minLength ):
		break

numNames = 0

while ( True ):
	numNames = int( input( "Number of names?" ) )

	if ( numNames > 0 ):
		break

'''

fileName = boysFileName
minLength = 4
maxLength = 10
numNames = 10

NameList = readFileIntoList( fileName )

FrequencyData = getFrequencyData( NameList )

NormalizedData = getNormalizedData( FrequencyData )

for index in range( 0, numNames ):
	print( generateName( NormalizedData, NameList, minLength, maxLength ) )
