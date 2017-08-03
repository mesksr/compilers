n = int(raw_input("Enter the number of non-terminals : "))
non_terminals = raw_input("Enter the non-terminals (separated by ',') : ").split(',')
first_pos = {}
follow_pos = {}


for i in range(n): 
    non_terminals[i] = non_terminals[i].strip()
    first_pos[non_terminals[i]] = []
    follow_pos[non_terminals[i]] = []

rules = {}
for i in range(n):
    temp = raw_input("Enter production rules for "+non_terminals[i]+" (separated by '|') : ")
    rules[non_terminals[i]] = []
    for rule in temp.split('|'):
        rules[non_terminals[i]].append(rule.strip())
    

    #------ removing left recursion start ------#
    beta = None
    for rule in rules[non_terminals[i]]:
        flag = False
        for e in rule:
             if (e in non_terminals):
                  flag = True
                  break
        if (not flag):
             beta = rule
             break

    count = 1
    rules_to_remove = []
    rules_to_add = []

    for rule in rules[non_terminals[i]]:
        if (rule[0] == non_terminals[i]):
            rules_to_remove.append(rule)
            alpha = rule[1:]
            new_symbol = non_terminals[i]+str(count)
            non_terminals.append(new_symbol)
            count += 1
            rules_to_add.append(beta+new_symbol)
            rules[new_symbol] = [alpha+new_symbol, None]
            print '\t', non_terminals[i], '->', rule, 'to',
            print non_terminals[i], '->', beta+new_symbol, '&', new_symbol, '->', alpha+new_symbol, None

    for temp in rules_to_remove:
        rules[non_terminals[i]].remove(temp)
    for temp in rules_to_add:
        rules[non_terminals[i]].append(temp)


    #------ TO DO --- removing left factoring start ------#

    
#------ finding first_pos ------#
def get_first_pos(nt):
    if (len(first_pos[nt]) == 0):
        for rule in rules[nt]:
            if (rule[0] not in non_terminals):
                first_pos[nt].append(rule[0])
            else:
                curr = 0
                while (True):
                    if (None not in get_first_pos(rule[0])):
                        first_pos[nt]+=get_first_pos(rule[0])
                        break
                    else:
                        curr+=1

    first_pos[nt] = list(set(first_pos[nt]))
    return first_pos[nt]

#------ finding follow_pos ------#
#def get_follow_pos(nt):
    #for p in 

starting_symbol = raw_input("Enter the starting symbol : ")
follow_pos[starting_symbol] = '$'

for nt in non_terminals:
    print "first_pos of", nt, "=", get_first_pos(nt)

d  = {}
for nt in non_terminals:
    for r in rules[nt]:
        d[(nt, first_pos.get(r[0],  r[0]))] = r
print d

string = raw_input("Enter string: ")
pos = 0
stack = ['$']
stack.append(starting_symbol)
while (True):
    l = stack.pop()
    if (l == '$'):
        print 'Accepted'
        break
    f = first_pos.get(string[pos], string[pos])
    if (l == f):
        print stack+[l], '&', string[pos], 'and matched'
        pos += 1
        continue
    print stack+[l], '&', string[pos], 'and ', l, f, '->', d[(l, f)]
    if (pos == len(string)):
        print "Accepted"
        break
    else:
        temp = list(d[(l, f)])
        temp = temp[::-1]
        stack += temp
