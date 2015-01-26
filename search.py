
import copy
from enum import Enum
from collections import deque
import time
import bisect

class Actions(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

	def ActionStr(action):
		if (action == Actions.UP): return "UP"
		if (action == Actions.DOWN): return "DOWN"
		if (action == Actions.LEFT): return "LEFT"
		if (action == Actions.RIGHT): return "RIGHT"

class boardState:

	'''initialize the numerals member variable as a 2D array representing the board state'''
	def __init__(self, numeralString):
		self.numerals = [[0,1,2],[3,4,5],[6,7,8]] # temp data
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
		
	#Return the state reached by moving the blank down
	def down(self):
		downState = copy.deepcopy(self)
		
		if (downState.blankRow == 2):
			return None
			
		downState.numerals[downState.blankRow][downState.blankColumn] = downState.numerals[downState.blankRow + 1][downState.blankColumn]
		downState.numerals[downState.blankRow + 1][downState.blankColumn] = 0

		downState.blankRow += 1
		
		return downState

	#Return the state reached by moving the blank up
	def up(self):
		upState = copy.deepcopy(self)
		
		if (upState.blankRow == 0):
			return None
			
		upState.numerals[upState.blankRow][upState.blankColumn] = upState.numerals[upState.blankRow - 1][upState.blankColumn]
		upState.numerals[upState.blankRow - 1][upState.blankColumn] = 0

		upState.blankRow -= 1
		
		return upState

	#Return the state reached by moving the blank left
	def left(self):
		leftState = copy.deepcopy(self)
		
		if (leftState.blankColumn == 0):
			return None
			
		leftState.numerals[leftState.blankRow][leftState.blankColumn] = leftState.numerals[leftState.blankRow][leftState.blankColumn - 1]
		leftState.numerals[leftState.blankRow][leftState.blankColumn - 1] = 0

		leftState.blankColumn -= 1
		
		return leftState

	#Return the state reached by moving the blank right
	def right(self):
		rightState = copy.deepcopy(self)
		
		if (rightState.blankColumn == 2):
			return None
			
		rightState.numerals[rightState.blankRow][rightState.blankColumn] = rightState.numerals[rightState.blankRow][rightState.blankColumn + 1]
		rightState.numerals[rightState.blankRow][rightState.blankColumn + 1] = 0

		rightState.blankColumn += 1
		
		return rightState

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

	def __init__(self, _parent, _data, _action):
		self.parent = _parent
		self.data = _data
		self.action = _action

		self.children = []
		self.depth = 0

		if self.parent is not None:
			self.parent.children.append(self)
			self.depth = self.parent.depth + 1

	def __str__(self):
		return "Node:\n" + str(self.data)

	def successor(self):
		retList = []

		successorData = self.data.up()
		if (successorData is not None):	retList.append(node(self, successorData, Actions.UP))
		successorData = self.data.down()
		if (successorData is not None):	retList.append(node(self, successorData, Actions.DOWN))
		successorData = self.data.left()
		if (successorData is not None):	retList.append(node(self, successorData, Actions.LEFT))
		successorData = self.data.right()
		if (successorData is not None):	retList.append(node(self, successorData, Actions.RIGHT))

		return retList

	def __eq__(self, other):
		return self.data == other.data

	def __hash__(self):
		return hash(self.data)

class search:

	def __init__(self, initialState):
		self.initialState = initialState
		self.solutionList = None
		self.totalTime = 0
		self.maxListLength = 0
		self.solutionLength = 0
		self.nodeList = None
		self.nodeSet = None
		self.startTime = 0

	def findSolution(self):

		rootNode = node(None, initialState, None)

		self.nodeList = deque([rootNode])
		self.nodeSet = set([rootNode])

		self.startTime = time.time()

		while True:

			# pops off the first item
			currNode = self.nodeList.popleft()

			if (currNode.data == goalState):
				self.saveSolution(currNode)
				return

			for successorNode in currNode.successor():
				self.addNodeToList(successorNode)

			if (len(self.nodeList) % 10 == 0):
				print(len(self.nodeList))
				
		# Control should only flow here if every node has been evaluated and no solution is found
		self.solutionList = None

	def addNodeToList(self, nodeToAdd):

		if nodeToAdd not in self.nodeSet: # check for duplicates
		
			self.addNodeToListPolyMorph(nodeToAdd) # "pure virtual" function for each search

			self.nodeSet.add(nodeToAdd) # Add to the set to check for duplicates

			currListLength = len(self.nodeList)

			if (currListLength > self.maxListLength):
				self.maxListLength = currListLength

	def saveSolution(self, currNode):
		print("Solution Found!")

		endTime = time.time()

		# Walk up the tree to get the solution steps

		self.solutionList = []

		while (currNode is not None):
			if (currNode.action is not None):
				self.solutionList.append(currNode)
			currNode = currNode.parent

		# Reverse the list so the solution is output correctly

		self.solutionList.reverse()

		# Store everything to be printed
		self.totalTime = endTime - self.startTime
		self.solutionLength = len(self.solutionList)

	def printSolution(self):

		if (self.solutionList is None):
			return

		print("Initial State:")
		print(self.initialState)
		print("") # blank line

		# Print the solution

		for solutionNode in self.solutionList:
			#print(solutionNode)
			print(Actions.ActionStr(solutionNode.action))

		print("Total time = {0} Solution length = {1} Max List Length: {2}".format(self.totalTime, self.solutionLength, self.maxListLength))

class greedyBestSearch(search):

	def __init__(self, initialState):
		self.initialState = initialState
		self.solutionList = None
		self.totalTime = 0
		self.maxListLength = 0
		self.solutionLength = 0
		self.nodeList = None
		self.nodeSet = None
		self.startTime = 0
		self.keys = [] # list used to store the results of the heuristic function

	def addNodeToListPolyMorph(self, nodeToAdd):

		heuristicResult = h1(nodeToAdd)

		# self.keys and self.nodeList are parralel deques. Store the heuristic results in
		# self.keys and use that to search for the index to insert the next node into
		insertionIndex = bisect.bisect_left(self.keys, heuristicResult)

		# Convert from deques to lists so the new items can be inserted
		nodeListList = list(self.nodeList)
		keysList = list(self.keys)

		# Insert the relevant items into the lists at the same index
		nodeListList.insert(insertionIndex, nodeToAdd)
		keysList.insert(insertionIndex, heuristicResult)

		# Convert back to deques
		self.nodeList = deque(nodeListList)
		self.keys = deque(keysList)

class aStarSearch(search):

	def addNodeToListPolyMorph(self, nodeToAdd):

		self.nodeList.append(nodeToAdd) # A*
		self.nodeList = deque(sorted(list(self.nodeList), key = f)) # sort by the f() function

class depthFirstSearch(search):

	def addNodeToListPolyMorph(self, nodeToAdd):

		self.nodeList.appendleft(nodeToAdd) # depth first.  Pushes onto the front

class breadthFirstSearch(search):

	def addNodeToListPolyMorph(self, nodeToAdd):

		self.nodeList.append(nodeToAdd) # breadth first.  Pushes onto the back

goalState = boardState("1 2 3 8 0 4 7 6 5")

# Heuristic 1. Number of tiles out of place. Used to estimate the cost of going from the given node to the goal node
def h1(node):

	diffCount = 0

	for row in range(3):
		for col in range(3):
			if (node.data.numerals[row][col] != goalState.numerals[row][col]):
				diffCount += 1

	return diffCount

# Cost of going from the initial node to the given node
def g(node):
	return node.depth

# Estimated cost to go from the initial node to the goal node through the given node
def f(node):
	return g(node) + h1(node)

while(True):

	inputNum = int(input("\nWhat would you like to do?\n"
					+ "\t0: Quit\n"
					+ "\t1: Run the easy problem\n"
					+ "\t2: Run the medium problem\n"
					+ "\t3: Run the hard problem\n"
					+ "\t4: Input a new problem\n"))

	initialState = None

	if (inputNum == 1):
		# easy
		initialState = boardState("1 3 4 8 6 2 7 0 5")
	elif (inputNum == 2):
		# medium
		initialState = boardState("2 8 1 0 4 3 7 6 5")
	elif (inputNum == 3):
		# hard
		initialState = boardState("5 6 7 4 0 8 3 2 1")
	elif (inputNum == 4):
		# custom
		initialState = boardState(input("Input a numeral list (e.g. 1 2 3 4 5 6 7 8 0)\n"))
	else:
		print("Invalid input")
		continue # return to input

	inputNum = int(input("What kind of search would you like to do?\n"
					+ "\t1: Depth First\n"
					+ "\t2: Breadth First\n"
					+ "\t3: Greedy Best First\n"
					+ "\t4: A*\n"))

	searchObj = None

	if (inputNum == 1):
		searchObj = depthFirstSearch(initialState)
	elif (inputNum == 2):
		searchObj = breadthFirstSearch(initialState)
	elif (inputNum == 3):
		searchObj = greedyBestSearch(initialState)
	elif (inputNum == 4):
		searchObj = aStarSearch(initialState)
	else:
		print("Invalid input")
		continue # return to input

	searchObj.findSolution()
	searchObj.printSolution()
