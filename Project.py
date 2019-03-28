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
        #Concatenate
        if c == '.':
            #Pop 2 nfas off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            #Connect nfa1 accept edge to nfa2 initial
            nfa1.accept.edge1 = nfa2.initial

            #Create new nfa and add back to the stack
            newNFA = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newNFA)
        #OR
        elif c == '|':
            #Pop 2 nfas off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            #Create 2 new states, 1 inital and 1 accept
            initial = state()
            accept = state()

            #Connect new initial to the each nfa initial
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            #Connect edge of nfa accept state to new accept state
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            #Create new nfa and add back to the stack
            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        #0 or many
        elif c == '*':
            #Pop one nfa off the stack
            nfa1 = nfastack.pop()

            #Create 2 new states, 1 inital and 1 accept
            initial = state()
            accept = state()

            #E arrows
            #Connect new initial to nfa1 inital
            initial.edge1 = nfa1.initial
            #Accept if string is empty
            initial.edge2 = accept

            #Connecting back to the initial state 
            nfa1.accept.edge1 = nfa.initial
            #String is accepted
            nfa1.accept.edge2 = accept

            #Create new nfa and add back to the stack
            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        #Other Characters
        else: 
            
            #Create 2 new states, 1 inital and 1 accept
            accept = state()
            initial = state()

            #Initial label = character that is not one of the operators
            initial.label = c
            #Connect initial directly to the accept state
            initial.edge1 = accept

            #Create new nfa and add back to the stack
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