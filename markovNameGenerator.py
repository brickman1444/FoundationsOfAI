
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

def getFrequencyData( nameList, order ):

	frequencyData = {}

	createEmptyCharacterDictionary( frequencyData, order )

	subslice = ""
	walkingIndex = 0

	for name in nameList:
		for subsliceStartingIndex in range( 0, len( name ) - order ):

			subslice = name[ subsliceStartingIndex : subsliceStartingIndex + order + 1 ]

			if ( subslice[ 0 ] == endCharacter ):
				# end of word. Exit early so we don't walk off the end
				break

			addToFrequencyData( frequencyData, subslice )

	return frequencyData

def createEmptyCharacterDictionary( dictionary, order ):
	
	if ( order == 0 ):
		setZeroForAllCharacters( dictionary )
	else:
		addEntryForAllCharacters( dictionary )

		for char in allCharacters:
			createEmptyCharacterDictionary( dictionary[ char ], order - 1 )

def addToFrequencyData( dictionary, substring ):

	if ( len( substring ) == 1 ):
		dictionary[ substring ] += 1
	else:
		addToFrequencyData( dictionary[ substring[ 0 ] ], substring[1:] )

def getNormalizedData( frequencyData, order ):

	normalizedData = {}

	createEmptyCharacterDictionary( normalizedData, order )

	normalizeDataRow( frequencyData, normalizedData, order )

	return normalizedData

def normalizeDataRow( frequencyData, normalizedData, order ):
	if ( order == 0 ):
		
		sum = 0

		for char in allCharacters:
			sum += frequencyData[ char ]

		if ( sum == 0 ):
			# avoid division by zero error
			return

		for char in allCharacters:
			normalizedData[ char ] = float( frequencyData[ char ] ) / float( sum )

	else:
		for char in allCharacters:
			normalizeDataRow( frequencyData[ char ], normalizedData[ char ], order - 1 )

def generateName( normalizedData, nameList, minLength, maxLength, order ):

	initialPrefix = ""

	for i in range( 0, order ):
		initialPrefix += startCharacter

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
		return generateName( normalizedData, nameList, minLength, maxLength, order )
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
order = 2

NameList = readFileIntoList( fileName )

FrequencyData = getFrequencyData( NameList, order )

NormalizedData = getNormalizedData( FrequencyData, order )

print( NormalizedData["e"]["r"] )

for index in range( 0, numNames ):
	print( generateName( NormalizedData, NameList, minLength, maxLength, order ) )

