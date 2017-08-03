# limitation - can take single char - S' is not accepted

n = int(raw_input("Enter the number of non-terminals : "))
non_terminals = raw_input("Enter the non-terminals (separated by ',') : ").split(',')

m = int(raw_input("Enter the number of terminals : "))
terminals = raw_input("Enter the terminals (separated by ',') : ").split(',')

# cleaning white-spaces
for i in range(n):
    non_terminals[i] = non_terminals[i].strip()
    
for i in range(m):
    terminals[i] = terminals[i].strip()

rules = {}
for i in range(n):
    temp = raw_input("Enter production rules for "+non_terminals[i]+" (separated by '|') : ")
    rules[non_terminals[i]] = []
    for rule in temp.split('|'):
        rules[non_terminals[i]].append(rule.strip())

#rules = {'S':['(L)', 'a'], 'L':['S', 'L,S']}

starting_symbol = raw_input("Enter starting symbol : ")

# adding auxilary rule @ -> ...$
rules['@'] = starting_symbol+'$'

states = []
g = {}

def create_state(start_rules):
    state = []
    for sr in start_rules:
        state.append(sr)
        
    while (True):
        flag = True
        rules_to_add = []
        for r in state:
            pos = r.find('.')
            if (pos == len(r)-1):
                continue
            sym = r[pos + 1]
            if sym in non_terminals:
                for sym_r in rules[sym]:
                    new_rule = sym+'->.'+sym_r
                    if (new_rule not in state):
                        rules_to_add.append(new_rule)
        if (len(rules_to_add) == 0):
            break
        else:
            state = state + rules_to_add
            
        
    if (state not in states):
        print ''
        print 'state', len(states) + 1, ':'
        for e in state:
            print e
            
        states.append(state)
        source = len(states)
        
        for next_e in non_terminals + terminals:
            start_rules = []
            for r in state:
                pos = r.find('.')
                if (pos == len(r)-1):
                    continue
                if (next_e == r[pos+1]):
                    start_rules.append(r[:pos] + next_e + '.' + r[pos+2:])
            if (len(start_rules) != 0):
                dest = create_state(start_rules)
                g[(source, next_e)] = dest
        return source
    else:
        return states.index(state)+1
            
                    
        

# sending first rule
create_state(['@->.' + starting_symbol+'$'])

# printing dfa
print '\ndfa :'
for k, v in g.items():
    print k, v

print '\nrules :'
# numbering rules [1, 2, 3....]
num_rules = [None]
for nt in non_terminals:
    for r in rules[nt]:
        num_rules.append(nt+'->'+r+'.')
        print len(num_rules)-1, num_rules[-1]


# adding these for display in table
terminals.append('$')
non_terminals.append('@')

print '\ntable\n\t|\t',
for e in terminals:
    print e,'\t',
print '|\t',
for e in non_terminals:
    print e,'\t',
print ''

table = {}
# accept
for i in range(1, len(states)+1):
    if '@->' + starting_symbol+'.$' in states[i-1]:
        table[i, '$'] = 'acc'
        break
    
for i in range(1, len(states)+1):

    # reduce
    for r in states[i-1]:
        if (r[-1] == '.'):
            pos = num_rules.index(r)
            for e in terminals:
                table[(i, e)] = 'r'+str(pos)

    # shift        
    print i, '\t|\t', 
    for e in terminals:
        if (g.get((i, e), False)):
            table[(i, e)] = 's'+str(g[(i, e)])
        print table.get((i, e), '_'),'\t',
    print '|\t',

    # goto
    for e in non_terminals:
        if (g.get((i, e), False)):
            table[(i, e)] = 'g'+str(g[(i, e)])
        print table.get((i, e), '_'),'\t',
    print ''


s = raw_input("\nEnter string to parse : ")+'$'
stack = [1]
p = 0
c = 0
while (True):
    c += 1
    if (c >= 100000):
        print 'cannot process'
        break
    print s, p, '->', s[p], 'and', stack[-1], '->', stack,  
    curr = table[(stack[-1], s[p])]
    print '::', curr
    if (curr == 'acc'):
        print 'accepted'
        break
    else:
        curr_x = curr[0]
        curr_y = int(curr[1:])
        if (curr_x == 's' or curr_x == 'g'):
            p += 1
            stack.append(curr_y)
        else:
            r = num_rules[curr_y]
            p1, p2 = r.split('->')
            p2 = p2[:-1]
            #print p1, p2, ':::', 
            temp = s[:p].rfind(p2)
            #print p, s[:p], temp,':::', s, '->', 
            s = s[:temp] + p1 + s[p:]
            p -= len(p2)
            stack = stack[:-len(p2)]
            #print s, stack
    #raw_input()
