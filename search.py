
import copy

class boardState:

	'''initialize the numerals member variable as a 2D array representing the board state'''
	def __init__(self, numeralString):
		self.numerals = [[0,1,2],[3,4,5],[6,7,8]]
	
		numeralList = numeralString.split(" ")
		
		if (len(numeralList) != 9):
			print("Error: Incorrect string input for boardstate.\n")
			return
		
		for index in range(0,9):
			column = index % 3
			row = index // 3 # integer part of division
			#print(index, row, column)
			self.numerals[row][column] = int(numeralList[index])
		
		
	def __str__(self):
	
		numeralList = []
		
		for row in self.numerals:
			for column in row:
				if (column != 0):
					numeralList.append(column)
				else:
					numeralList.append(" ")
		
		retString = '''-------\n|{0}|{1}|{2}|\n-------\n|{3}|{4}|{5}|\n-------\n|{6}|{7}|{8}|\n-------'''.format(*numeralList)
		return retString
		
	def __eq__(self, other):
		print(self.numerals)
		print(other.numerals)
		for row in range(3):
			for column in range(3):
				if (int(self.numerals[row][column]) != int(other.numerals[row][column])):
					return False
		return True
		
	'''Return the state reached by moving a piece up into the blank'''
	def up(self):
		upState = copy.deepcopy(self)
		
		blankRow = -1
		blankColumn = -1
		
		for row in range(3):
			for column in range(3):
				if (upState.numerals[row][column] == 0):
					blankRow = row
					blankColumn = column
					break
		
		if (blankRow == 2):
			return None
			
		upState.numerals[blankRow][blankColumn] = upState.numerals[blankRow + 1][blankColumn]
		upState.numerals[blankRow + 1][blankColumn] = 0
		
		return upState
		

#board = boardState(input("Input a numeral list\n"))
board1 = boardState("1 2 3 0 5 6 7 8 4")
print(board1)
print(board1.up())
print(board1)