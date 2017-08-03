count = 0 # for labels
d = {} # relate label to node
ips = [] # input symbols

def calcFollowpos(x, fp):
        if (len(x.children) == 0):
                x.followpos = fp
        elif (len(x.children) == 1):
                calcFollowpos(x.children[0], fp+x.children[0].firstpos)
        elif (x.val == '.'):
                calcFollowpos(x.children[0], x.children[1].firstpos)
                calcFollowpos(x.children[1], fp)
        else:
                calcFollowpos(x.children[0], fp)
                calcFollowpos(x.children[1], fp)
        
def dfs(x):
        if (len(x.children) == 0):
                print '\tvalue =', x.val, '- - - label =', x.label, '- - - nullable =', x.nullable, '- - - firstpos =', x.firstpos,
                print '- - - lastpos =', x.lastpos, '- - - followpos =', x.followpos
        elif (len(x.children) == 1):
                dfs(x.children[0])
                print '\tvalue =', x.val, '- - - label = N.A.- - - nullable =', x.nullable, '- - - firstpos =', x.firstpos,
                print '- - - lastpos =', x.lastpos, '- - - followpos = N.A.'
        else:
                dfs(x.children[0])
                print '\tvalue =', x.val, '- - - label = N.A.- - - nullable =', x.nullable, '- - - firstpos =', x.firstpos,
                print '- - - lastpos =', x.lastpos, '- - - followpos = N.A.'
                dfs(x.children[1])
                
class node:
        def __init__(self, data):
                global count, ip
                #print data
                self.followpos = ''
                if (len(data) == 3):
                        self.val = data[1]
                        if (data[0].isalpha()):
                                leftNode = node([data[0]])
                                d[int(leftNode.label)] = leftNode
                        else:
                                leftNode = data[0]
                        if (data[2].isalpha() or data[2] == '$'):
                                rightNode = node([data[2]])
                                d[int(rightNode.label)] = rightNode
                        else:
                                rightNode = data[2]
                        self.children = [leftNode, rightNode]

                        leftNullable = self.children[0].nullable
                        leftFirstpos = self.children[0].firstpos
                        leftLastpos = self.children[0].lastpos

                        rightNullable = self.children[1].nullable
                        rightFirstpos = self.children[1].firstpos
                        rightLastpos = self.children[1].lastpos

                        if (self.val == '|'):
                                self.nullable = leftNullable or rightNullable
                                self.firstpos = leftFirstpos + rightFirstpos
                                self.lastpos = leftLastpos + rightLastpos
                                self.children[0].followpos = self.followpos
                                self.children[1].followpos = self.followpos
                        elif (self.val == '.'):
                                self.nullable = leftNullable and rightNullable
                                if (leftNullable):
                                        self.firstpos = leftFirstpos + rightFirstpos
                                else:
                                        self.firstpos = leftFirstpos
                                if (rightNullable):
                                        self.lastpos = leftLastpos + rightLastpos
                                else:
                                        self.lastpos = rightLastpos
                                        
                elif(len(data) == 2):
                        self.val = data[1]
                        if (data[0].isalpha()):
                                childNode = node([data[0]])
                                d[int(childNode.label)] = childNode
                        else:
                                childNode = data[0]
                        self.children = [childNode]
                        
                        if (self.val == '*'):
                                self.nullable = True
                                self.firstpos = self.children[0].firstpos
                                self.lastpos = self.children[0].lastpos
                                
                else:
                        ips.append(data[0])
                        self.val = data[0]
                        count += 1
                        self.label = str(count)+' '
                        print '\t value =', data[0], 'label =', count
                        self.children = []
                        self.nullable = False
                        self.firstpos = str(count)+' '
                        self.lastpos = str(count)+' '
                        

        def isalpha(self):
                return False

        

s = raw_input("Enter reg-ex : ")
stack = ['$']
print '\nnode to label :' 
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
                
calcFollowpos(stack[1], '')
print '\nin-order traverse :'
dfs(stack[1])

#print '\nlabel to node :'
#for k, v in d.items():
#        print '\t', 'label =', k, 'value =', v.val

ips = list(set(ips))
states = [tuple(sorted(map(int, stack[1].firstpos.split())))]
marked = {}

print '\ncreating dfa :'
while (True):
        T = None
        for s in states:
                if (not marked.get(s, False)):
                        T = s
                        break
        if (T is None):
                break
        marked[T] = True

        
        for ip in ips:
                temp = []
                for e in T:
                        #print e, '->', d[e].val, ',', 
                        if (d[e].val == ip):
                                temp += map(int, d[e].followpos.split())
                if (len(temp) > 0):
                        temp = tuple(set(sorted(temp)))
                        print '\t', T, '---'+str(ip)+'-->', temp
                        if (temp not in states):
                                states.append(temp)
                

print '\nstates :\n\t', states
print '\ninput sybmols :\n\t', ips

