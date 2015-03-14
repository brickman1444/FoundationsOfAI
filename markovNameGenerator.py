
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

# Set the dictionary entry for all valid characters to 0.
# Used on the leaf level of the frequency and normalized data dictionaries
def setZeroForAllCharacters( dictionary ):
	for char in allCharacters:
		dictionary[ char ] = 0

# Fills out an empty nested dictionary to the right depth
# the leaf entries are all set to 0.
# Used to initialize the frequency data and normalized data
# Final result looks like dictionary["a"]["a"] ... ["a"] = 0 for all possible letter combinations
def createEmptyCharacterDictionary( dictionary, order ):
	
	if ( order == 0 ):
		setZeroForAllCharacters( dictionary )
	else:
		addEntryForAllCharacters( dictionary )

		for char in allCharacters:
			createEmptyCharacterDictionary( dictionary[ char ], order - 1 )

# parse through an input file and return a list of all the names
# adds the padding characters to the ends of each name in the list
def readFileIntoList( fileName, order ):

	nameList = []

	file = open( fileName, "r" )

	for line in file:

		line = line.replace("\n","")

		line = addPaddingCharacters( line, order )

		line = line.lower()

		nameList.append( line )

	file.close()

	return nameList

# Add the start and end characters to the front and back of the name
# Scales with the order number
# e.g. order 3 and Zac would output "<<<Zac>>>"
def addPaddingCharacters( name, order ):

	retName = name

	for i in range( 0, order ):
		retName = startCharacter + retName + endCharacter

	return retName

# Takes a list of names and calculates the frequency data of how often
# given characters follow other characters. Returns a nested dictionary
# of the data
def getFrequencyData( nameList, order ):

	frequencyData = {}

	createEmptyCharacterDictionary( frequencyData, order )

	subslice = ""

	for name in nameList:
		for subsliceStartingIndex in range( 0, len( name ) - order ):

			subslice = name[ subsliceStartingIndex : subsliceStartingIndex + order + 1 ]

			addToFrequencyData( frequencyData, subslice )

	return frequencyData

# Recursively go down the frequency data until the leaf level is reached
# increment the lowest level and then return all the way back up
# e.g. a a substring of "acha" would increment dictionary["a"]["c"]["h"]["a"]
def addToFrequencyData( dictionary, substring ):

	if ( len( substring ) == 1 ):
		dictionary[ substring ] += 1
	else:
		addToFrequencyData( dictionary[ substring[ 0 ] ], substring[1:] )

# Takes the frequency data and turns it into a probability table
# Makes the leaf layer rows stochastic. 
def getNormalizedData( frequencyData, order ):

	normalizedData = {}

	createEmptyCharacterDictionary( normalizedData, order )

	normalizeDataRow( frequencyData, normalizedData, order )

	return normalizedData

# recursively go down the normalized data dictionary
# sum up the frequencies and calculate the probabilities
# of each entry. Store these probabilities in the normalized
# data.
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

# Generate a name given the parameters. Limits the name to
# within the min and max length and only allows unique names
# that aren't on the original name list
def generateName( normalizedData, nameList, minLength, maxLength, order ):

	initialPrefix = ""

	for i in range( 0, order ):
		initialPrefix += startCharacter

	# generated name starts with an initial prefix like "<<<"
	generatedName = initialPrefix

	nextChar = getRandomCharacter( normalizedData, generatedName[ -order : ] )

	while ( not nextChar == endCharacter ):
		generatedName += nextChar
		nextChar = getRandomCharacter( normalizedData, generatedName[ -order : ] )

	generatedName = generatedName.replace( initialPrefix, "" )

	nameLength = len( generatedName )

	if ( nameLength < minLength or nameLength > maxLength or addPaddingCharacters( generatedName, order ) in nameList):

		# Outside of range. Regenerate.
		return generateName( normalizedData, nameList, minLength, maxLength, order )
	else:
		return generatedName

# Recursively go down the normalized data to the leaf layer 
# to pick what letter should go next.
def getRandomCharacter( normalizedData, subslice ):

	if ( len( subslice ) == 1 ):

		randVal = random()

		partialSum = 0

		for char in allCharacters:

			partialSum += normalizedData[ subslice ][ char ]

			if ( randVal < partialSum ):
				return char

	else:
		return getRandomCharacter( normalizedData[ subslice[ 0 ] ], subslice[ 1 : ] )

def countEmptySpots( dictionary, order ):
		
	if ( order == 0 ):

		sum = 0

		for char in allCharacters:
			if dictionary[ char] == 0:
				sum += 1

		return sum
	else:
		sum = 0

		for char in allCharacters:
			sum += countEmptySpots( dictionary[ char ], order - 1 )

		return sum

def countAllSpots( dictionary, order ):

	if ( order == 0 ):

		sum = 0

		for char in allCharacters:
			sum += 1

		return sum
	else:
		sum = 0

		for char in allCharacters:
			sum += countAllSpots( dictionary[ char ], order - 1 )

		return sum

# Begin main code

'''
# Non-UI input
fileName = girlsFileName
minLength = 4
maxLength = 10
numNames = 10
order = 3
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

order = 0

while ( True ):
	order = int( input( "Order?" ) )

	if ( order > 0 ):
		break

NameList = readFileIntoList( fileName, order )

FrequencyData = getFrequencyData( NameList, order )

NormalizedData = getNormalizedData( FrequencyData, order )

while ( True ):

	for index in range( 0, numNames ):
		print( generateName( NormalizedData, NameList, minLength, maxLength, order ) )

	rerun = input( "Run again? (y/n)" )

	if ( rerun != "y" ):
		break

