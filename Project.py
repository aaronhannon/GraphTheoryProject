#Graph Theory Project - G00347352 - Aaron Hannon

#Shunting algorithm

def shunt(infix):
    #Specials
    specials = {'*': 50, '.': 40, '|':30}
    stack = ""
    postfix = ""
    
    for c in infix:
        if c == '(':
            #Adding Left bracket to the stack
            stack = stack + c
        elif c == ')':
            #Pop everything off the stack until left bracket is met
            while stack[-1] != '(':
                postfix,stack = postfix + stack[-1],stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            #while stack isnt empty and character value is 
            # less than the value of the last character on the stack
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                postfix,stack = postfix + stack[-1],stack[:-1]
            #add it to the stack
            stack = stack + c
        # If c is not a special or bracket it is just added to the postfix string 
        else:
            postfix = postfix + c
    #Clear stack and add to postfix
    while stack:
        postfix,stack = postfix + stack[-1],stack[:-1]
    return postfix

class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(postfix):
    nfastack = []

    for c in postfix:
        if c == '.':

            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            nfa1.accept.edge1 = nfa2.initial

            newNFA = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newNFA)
        elif c == '|':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            accept = state()

            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        elif c == '*':
            nfa1 = nfastack.pop()

            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            nfa1.accept.edge1 = nfa.initial
            nfa1.accept.edge2 = accept

            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        else:

            accept = state()
            initial = state()

            initial.label = c
            initial.edge1 = accept


            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)

    return nfastack.pop()

def followes(state):
    states = set()
    states.add(state)

    if state.label is None:
        if state.edge1 is not None:
            states |= followes(state.edge1)
        if state.edge2 is not None:
            states |= followes(state.edge2)

    return states


def match(infix,string):
    postfix = shunt(infix)
    nfa = compile(postfix)

    current = set()
    next = set()

    current |= followes(nfa.initial)

    for s in string:
        for c in current:
            if c.label == s:
                next |= followes(c.edge1)

        current = next
        next = set()

    return (nfa.accept in current)

infixes = ["a.b.c*","a.(b|d).c*","(a.(b|d))*","a.(b.b)*.c"]
strings = ["","abc","abbc","abcc","abad","abbbc"]

shunting = shunt("a.(b|d).c*")
print(shunting)

print(compile(shunting))

for i in infixes:
    for s in strings:
        print(match(i,s),i,s)