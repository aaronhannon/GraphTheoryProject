# 3rd Year Graph Theory Project
## My Details
* Name: Aaron Hannon
* ID: G00347352

### Project description
Write a Python Program that can build a non-deterministic finite automaton (NFA) from a Infix or Postfix expression. This NFA can be used to check if the expression matches any string of text that is given from the user or from a text file.

# How The Code Works:
1. The Shunt function takes in an infix expression as a parameter. A for loop then loops through the expression looking for special characters, regular characters and brackets. If a special character is encountered it is added to the stack. If a regular character is met it is added to the postfix string and if a closing bracket is found it pops the stack and adds everything to the postfix string in order of precedence. Then the post fix expression us returned.

2. The Compile function is Thompson's Algorithm. A postfix expression is passed in as a parameter, the expression is then looped over looking for special operators e.g "+", "?", "|" etc. Once one of these operators is met it creates nfa's related to the operator and adds them to a stack. If at the end of the expression, it returns the single nfa object left on the stack

3. When the match function is called it takes in 3 parameters (setting,expression,string) setting just switches between infix and postfix, the second one is the expression itself and the third is the string that you want to match to the expression. This function also calls the shunt and Compile functions which return an nfa that can be used to match the string. Then it creates 2 states, the current state is set to the nfas initial state through the followes function which just returns the set of paths/states related to the parameter you pass in. It loops through the string comparing the character to the label of the current states. At the end a "True" Or "False" is returned if a match is found.

4. Is a User Interface/Menu I added with some extra functionality.

# Extras
1. (+) Plus Operator (One or More)
2. (?) Question Mark Operator (0 or 1)
3. User Interface / Menu


	
	 MENU
	======
	1. View Examples
	2. Enter Infix Expression
	3. Enter Postfix Expression
	4. Read from file(Sample Provided in Project folder)
	5. Exit
	Option:




  ###### WHAT DO THESE OPTIONS DO?
  1. Allows the user to see some examples of the program in action.
  2. Allows the user to enter there own infix expression along with a string of their choice.
  3. Allows the user to enter there own postfix expression along with a string of their choice.
  4. Allows the user to enter the file path of a list of infix expression and a file path of a list of strings and it will match the nfa to the string.
  5. Exits the Program.


  # Research

  1. I had a look at this tutorial on w3schools https://www.w3schools.com/python/python_classes.asp to try and fully understand how classes worked

  2. Before programming I looked at this website to wrap my head around converting infix expressions to postfix ones. http://www.oxfordmathcenter.com/drupal7/node/628

  3. I had a look at the site to figure out how to do the "+" and "?" operators. Turns out it was very useful because it had diagrams to go along with some code. https://swtch.com/~rsc/regexp/regexp1.html

  4. I found this site useful as it gives a great explanation on how each of the operators work http://web.mit.edu/gnu/doc/html/regex_3.html. However they did not have any diagrams to demonstrate fully.

  5. As I wanted to add file reading functionality I had to do some research to figure out how to do it. Turns out it was pretty easy this is the tutorial on w3schools I followed: https://www.w3schools.com/python/python_file_open.asp

  6. When reading in from a file I encountered a bug that when reading in the expressions and strings where the .readLine() function seemed to store the white space too so I had to look up how to get rid of it. I knew java had a method to do this, python does too as I found out from this link: https://www.journaldev.com/23625/python-trim-string-rstrip-lstrip-strip. The .trim() method just removes any spaces or white space at the end of a string.

# How to run:
1. Download or clone the Repository
2. Extract if downloaded
3. Using any CLI navigate to the folder
4. Type "python.exe Project.py"
5. Use the menu as you wish
6. Press 5 to exit the program
