
boysFileName = "namesBoys.txt"
girlsFileName = "namesGirls.txt"

file = open( boysFileName, "r")

for line in file:
	print( line )

print("hello world")

file.close()