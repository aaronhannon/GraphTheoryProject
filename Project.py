#Graph Theory Project - G00347352 - Aaron Hannon

#Shunting algorithm - Converts infix expression to postfix expression
def shunt(infix):
    #Specials
    specials = {'+': 50, '?': 50, '*': 50, '.': 40, '|':30}
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

#State Class
class state:
    label = None
    edge1 = None
    edge2 = None

#Nfa Class
class nfa:
    initial = None
    accept = None

    #Constructor
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
            nfa1.accept.edge1 = nfa1.initial
            #String is accepted
            nfa1.accept.edge2 = accept

            #Create new nfa and add back to the stack
            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        #One or more
        elif c == '+':
            #Pop one nfa off the stack
            nfa1 = nfastack.pop()

            #Create 2 new states, 1 inital and 1 accept
            initial = state()
            accept = state()

            #E arrows
            #Connect new initial to nfa1 inital
            initial.edge1 = nfa1.initial

            #Connecting back to the initial state 
            nfa1.accept.edge1 = nfa1.initial
            #String is accepted
            nfa1.accept.edge2 = accept

            #Create new nfa and add back to the stack
            newNFA = nfa(initial, accept)
            nfastack.append(newNFA)
        #0 or 1
        elif c == '?':
            #Pop one nfa off the stack
            nfa1 = nfastack.pop()

            #Create 2 new states, 1 inital and 1 accept
            initial = state()
            accept = state()

            #E arrows
            #Accept if string is empty
            initial.edge2 = accept
            #Connect new initial to nfa1 inital
            initial.edge1 = nfa1.initial
            
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
    #Create set for states
    states = set()
    states.add(state)

    #if state is not null, set states set to states next states 
    if state.label is None:
        if state.edge1 is not None:
            states |= followes(state.edge1)
        if state.edge2 is not None:
            states |= followes(state.edge2)

    return states


def match(setting,expression,string):
    if setting == 1:
        #Converts infix expression to postfix
        postfix = shunt(expression)
        #Creates an nfa from a given postfix expression 
        nfa = compile(postfix)
    elif setting == 2:
        #Sets expression to postfix variable
        postfix = expression
        #Creates an nfa from a given postfix expression 
        nfa = compile(postfix)
    #Creates 2 sets
    current = set()
    next = set()
    #Sets current to inital states
    current |= followes(nfa.initial)

    for s in string:
        for c in current:
            #if c.label equals s then set the next set to c's next states 
            if c.label == s:
                next |= followes(c.edge1)

        #Setting current set of states to next state
        current = next
        next = set()

    return (nfa.accept in current)

infixes = ["a.b.c*","a.b.c+","a.b.c?","a.(b|d).c?","(a.(b|d))*","a.(b.b)*.c"]
strings = ["","abcc","abbc","abcc","abad","abbbc"]

#Var to exit menu loop
exitBool = False

#MENU LOOP
while exitBool != True:
    print("\n======\n MENU \n======\n1. View Examples\n2. Enter Infix Expression\n3. Enter Postfix Expression\n4. Read from file(Sample Provided in Project folder)\n5. Exit")
    option = input("Option: ")

    #Samples from videos
    if option == "1":
        for i in infixes:
            for s in strings:
                print(match(1,i,s),i,s)
    #User can enter an infix expression followed by a string
    elif option == "2":
        infix = input("Enter Infix Expression:")
        string = input("Enter String:")
        print("Postfix: ",shunt(infix))
        print("\nMatch =",match(1,infix,string),"\nTO INFIX:",infix,"\nWITH STRING:",string)
    #User can enter a postfix expression followed by a string      
    elif option == "3":
        postfix = input("Enter Postfix Expression:")
        string1 = input("Enter String:")
        print("\nMatch =",match(2,postfix,string1),"\nTO POSTFIX:",postfix,"\nWITH STRING:",string1)
    #Read infix expressions and strings from txt files
    elif option == "4":
        infixFile = []
        stringFile = []

        infixPath = input("Enter infix file path(./Sample_Files/infixes.txt): ")
        stringPath = input("Enter string file path()./Sample_Files/strings.txt): ")

        f = open(infixPath, "r")
        for x in f:
            infixFile.append(x.strip())
        f.close()
        f = open(stringPath, "r")
        for x in f:
            stringFile.append(x.strip())
        f.close()
        for i in infixFile:
            for s in stringFile:
                print(match(1,i,s),i,s)
    #EXIT MENU
    elif option == "5":
        exitBool = True
            