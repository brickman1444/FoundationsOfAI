


class boardState:

	#numerals = [[0,1,2],[3,4,5],[6,7,8]]

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

#board = boardState(input("Input a numeral list\n"))
board1 = boardState("1 2 3 4 5 6 7 8 0")
board2 = boardState("1 2 3 4 5 6 7 8 0")
print(board1)
print(board2)
print(board1 == board2)