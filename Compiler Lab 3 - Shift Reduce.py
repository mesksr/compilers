def dfs(x):
	try:
		if (x in s):
			print x
	except:
		if (len(x.children) == 1):
			print x.val
			dfs(x.children[0])
		else:
			dfs(x.children[0])
			print x.val
			dfs(x.children[1])
class node:
	def __init__(self, data):
		if (len(data) == 3):
			self.val = data[1]
			self.children = [data[0], data[2]]
		else:
			self.val = data[0]
			self.children = [data[1]]

s = raw_input("Enter string: ")
stack = ['$']
for e in s:
	if (e != ')'):
		stack.append(e)
	else:
		curr = []
		while (True):
			if (stack[-1] == '('):
				stack = stack[:-1]
				break
			curr.append(stack[-1])
			stack = stack[:-1]
		curr = curr[::-1]
		newNode = node(curr)
		stack.append(newNode)
		#print stack, curr
print 'in-order traverse :'
dfs(stack[1])
		
