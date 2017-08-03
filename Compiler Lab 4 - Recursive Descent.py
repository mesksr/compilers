def f(string, pos, non_terminal):
    #print pos, '->', string[pos], non_terminal
    any_rule_satisfy = False
    #print non_terminal, '=', rules[non_terminal]
    for rule in rules[non_terminal]:
        #print '\t ******',rule, '******'
        temp = pos
        this_rule_satisfy = True
        for c in rule:
            if c in non_terminals:
                #print '\t\t', non_terminal, '=', rule, 'calling', c
                x, y = f(string, temp, c)
                #print '\t\t', non_terminal, '=', rule, 'got', (x, y), 'from', c
                if (x == False):
                    this_rule_satisfy = False
                    break
                else:
                    temp = y
            else:
                if (c == string[temp]):
                    #print '\t\tmatched', c, 'of', non_terminal, '=', rule 
                    temp += 1
                else:
                    #print '\t\tnot-matched', c, '&', string[temp], 'of', non_terminal, '=', rule
                    this_rule_satisfy = False
                    
        any_rule_satisfy = any_rule_satisfy or this_rule_satisfy
        if (any_rule_satisfy):
            print non_terminal, '=', rule
            break
        
    #print '\t\t','>>', non_terminal, 'returned', any_rule_satisfy
    return any_rule_satisfy, temp

n = int(raw_input("Enter the number of non-terminals : "))
non_terminals = raw_input("Enter the non-terminals (separated by ',') : ").split(',')

for i in range(n): 
    non_terminals[i] = non_terminals[i].strip()

rules = {}
for i in range(n):
    temp = raw_input("Enter production rules for "+non_terminals[i]+" (separated by '|') : ")
    rules[non_terminals[i]] = []
    for rule in temp.split('|'):
        rules[non_terminals[i]].append(rule.strip())

starting_symbol = raw_input("Enter the starting symbol : ")

string = raw_input("Enter string: ")

#print non_terminals, rules, starting_symbol, string

x, y = f(string, 0, starting_symbol)

if (y != len(string)):
    x = False

print x
