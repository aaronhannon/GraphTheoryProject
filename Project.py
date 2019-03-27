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

print(shunt("a.(b|d).c*"))