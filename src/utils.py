import sys

def get_distance(w0, w1):
	"""
	Returns the dictionary distance between two words.
	"""
	if w0 == w1:
		return 0

	dynamic_table = []
	for i in range(len(w0)+1):
		dynamic_table.append([0]* (len(w1)+1))

	for i in range(len(w0)):
		dynamic_table[i+1][0] = i+1
	for i in range(len(w1)):
		dynamic_table[0][i+1] = i+1

	insert_cost = 0
	delete_cost = 0
	replace_cost = 0
	transpose_cost = sys.maxsize

	substring0 = ''
	substring1 = ''

	for i in range(len(w0)):
		substring0 = substring0 + w0[i]
		substring1 = ''
		for j in range(len(w1)):
			substring1 = substring1 + w1[j]

			if substring0 == substring1:
				dynamic_table[i+1][j+1] = 0
			else:
				insert_cost = dynamic_table[i+1][j] + 1
				delete_cost = dynamic_table[i][j+1] + 1
				replace_cost = dynamic_table[i][j] + 1 if w0[i] != w1[j] else dynamic_table[i][j]
				if i>0 and j>0:
					transpose_cost = dynamic_table[i-1][j-1] if w0[i] == w1[j-1] and w0[i-1] == w1[j] else sys.maxsize
				dynamic_table[i+1][j+1] = min(insert_cost, delete_cost, replace_cost, transpose_cost)

	return dynamic_table[len(w0)][len(w1)]