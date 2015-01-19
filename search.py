
import copy
from enum import Enum
from collections import deque

#Action = Enum("UP","DOWN","LEFT","RIGHT")

class boardState:

	'''initialize the numerals member variable as a 2D array representing the board state'''
	def __init__(self, numeralString):
		self.numerals = [[0,1,2],[3,4,5],[6,7,8]]
		self.blankRow = -1
		self.blankColumn = -1
	
		numeralList = numeralString.split(" ")
		
		if (len(numeralList) != 9):
			print("Error: Incorrect string input for boardstate.\n")
			return
		
		for index in range(0,9):
			column = index % 3
			row = index // 3 # integer part of division
			#print(index, row, column)
			self.numerals[row][column] = int(numeralList[index])
			if (int(numeralList[index]) ==0):
				self.blankRow = row
				self.blankColumn = column
		
	def __str__(self):
	
		numeralList = []
		
		for row in self.numerals:
			for column in row:
				if (column != 0):
					numeralList.append(column)
				else:
					numeralList.append(" ")
		
		retString = "-------\n|{0}|{1}|{2}|\n-------\n|{3}|{4}|{5}|\n-------\n|{6}|{7}|{8}|\n-------".format(*numeralList)
		#retString += "Blank row: {0}, Blank col: {1}".format(self.blankRow, self.blankColumn)
		return retString
		
	def __eq__(self, other):

		#print(self.numerals)
		#print(other.numerals)
		for row in range(3):
			for column in range(3):
				if (int(self.numerals[row][column]) != int(other.numerals[row][column])):
					return False
		return True

	def __hash__(self):
		return hash(str(self.numerals))
		
	#Return the state reached by moving a piece up into the blank
	def up(self):
		upState = copy.deepcopy(self)
		
		if (upState.blankRow == 2):
			return None
			
		upState.numerals[upState.blankRow][upState.blankColumn] = upState.numerals[upState.blankRow + 1][upState.blankColumn]
		upState.numerals[upState.blankRow + 1][upState.blankColumn] = 0

		upState.blankRow += 1
		
		return upState

	#Return the state reached by moving a piece down into the blank
	def down(self):
		downState = copy.deepcopy(self)
		
		if (downState.blankRow == 0):
			return None
			
		downState.numerals[downState.blankRow][downState.blankColumn] = downState.numerals[downState.blankRow - 1][downState.blankColumn]
		downState.numerals[downState.blankRow - 1][downState.blankColumn] = 0

		downState.blankRow -= 1
		
		return downState

	#Return the state reached by moving a piece right into the blank
	def right(self):
		rightState = copy.deepcopy(self)
		
		if (rightState.blankColumn == 0):
			return None
			
		rightState.numerals[rightState.blankRow][rightState.blankColumn] = rightState.numerals[rightState.blankRow][rightState.blankColumn - 1]
		rightState.numerals[rightState.blankRow][rightState.blankColumn - 1] = 0

		rightState.blankColumn -= 1
		
		return rightState

	#Return the state reached by moving a piece left into the blank
	def left(self):
		leftState = copy.deepcopy(self)
		
		if (leftState.blankColumn == 2):
			return None
			
		leftState.numerals[leftState.blankRow][leftState.blankColumn] = leftState.numerals[leftState.blankRow][leftState.blankColumn + 1]
		leftState.numerals[leftState.blankRow][leftState.blankColumn + 1] = 0

		leftState.blankColumn += 1
		
		return leftState

	def successor(self):
		list = []

		state = self.up();
		if (state is not None): list.append(state)
		state = self.down();
		if (state is not None): list.append(state)
		state = self.right();
		if (state is not None): list.append(state)
		state = self.left();
		if (state is not None): list.append(state)

		return list
		

class node:
	parent = None
	children = []
	data = None

	def __init__(self, _parent, _data):
		self.parent = _parent
		self.data = _data

		if self.parent is not None:
			self.parent.children.append(self)

	def __str__(self):
		return "Node:\n" + str(self.data)

	def successor(self):
		retList = []
		for successorData in self.data.successor():
			retList.append(node(self, successorData))

		return retList

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash(self.data)


#board = boardState(input("Input a numeral list\n"))
goalState = boardState("1 2 3 8 0 4 7 6 5")

initialState = boardState("1 3 4 8 6 2 7 0 5") # easy
#initialState = boardState("2 8 1 0 4 3 7 6 5") # medium
#initialState = boardState("5 6 7 4 0 8 3 2 1") # hard

rootNode = node(None, initialState)

nodeList = deque([rootNode])
nodeSet = set([rootNode])

while True:

	# pops off the first item 
	currNode = nodeList.popleft()

	if (currNode.data == goalState):
		print("solution found")

		i = 0

		while (currNode is not None):
			print(i)
			i += 1
			print(currNode)
			currNode = currNode.parent

		break

	successors = currNode.successor()

	for successorNode in successors:

		if successorNode not in nodeSet:
			nodeList.append(successorNode)
			nodeSet.add(successorNode)

	print(len(nodeSet))
