from Stack import Stack
from Environment import Environment
from CSComponents import *

class CSEMachine:

    # The CSEMachine class simulates the Control Stack Environment machine for RPAL.
    # It interprets the control structures and manages environments, stack, and built-in functions.

    def __init__(self, control_structure, errors):
        # Initialize the CSEMachine with control structures and error handler.
        self.control_structures = control_structure
        self.errors = errors 

        # Initialize stack for computation
        self.stack = Stack()
        # Initialize control list for execution
        self.control = []
        # List of environments (for variable/function scope)
        self.environments = [Environment(0, None)]

        # Set up the initial environment and control
        self.current_environment = 0
        self.control.append(self.environments[0].name)
        self.control += self.control_structures[0]
        self.stack.push(self.environments[0].name)
        
        # Built-in functions and operation keywords
        self.built_in_functions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]
        self.binop = ["+", "-", "*", "/", "**", "gr", "ge","ls", "le", "eq", "ne", "or", "&", "aug"]
        self.unop = ["neg","not"]

        # State to track if a print command was called
        self.print_state = False
        

    def lookup(self, var):
        # Looks up the value of a variable or processes a literal.
        if var[:5] == "<INT:" and var[-1] == ">":
            return int(var[5:-1])
        elif var[:5] == "<STR:" and var[-1] == ">":
            return var[5:-1]
        elif var[:4] == "<ID:" and var[-1] == ">":
            if var[4:-1] in self.built_in_functions:
                return var[4:-1]
            else:
                return self.environments[self.current_environment].variables[var]     
        elif var[:2] == "Y*":
            return "Y*"
        elif var[:3] == "nil":
            return ()
        elif var[:4] == "true":
            return True
        elif var[:5] == "false":
            return False
        

    def apply_rules(self):
        # Main execution loop: applies the CSE machine rules to process the control structures.
        while len(self.control) > 0:

            # Update current environment from the stack
            for i in range(len(self.stack.items)):
                val = self.stack.items[len(self.stack.items)-i-1]
                if type(val) == str and val[:2] == "e_":
                    self.current_environment = int(val.split("_")[-1])
                    break

            # Pop the next element from the control
            element = self.control.pop()
    
            # Handle literals and identifiers
            if type(element) == str and element[0] == "<" and element[-1] == ">":
                self.stack.push(self.lookup(element))

            # Handle Lambda objects
            elif isinstance(element, Lambda):
                element.env = self.current_environment
                self.stack.push(element)
                
            # Handle gamma (function application and built-ins)
            elif type(element) == str and element[:5] == "gamma":
                
                element_1 = self.stack.pop()
                element_2 = self.stack.pop()

                # Lambda application
                if isinstance(element_1, Lambda):
                    parent_env = self.environments[element_1.env]
                    child_env = Environment(len(self.environments),parent_env)
                    parent_env.add_child(child_env)
                    self.environments.append(child_env)

                    variablesList = element_1.val
                    if(isinstance(variablesList, list)):
                        for i in range(len(variablesList)):
                            child_env.add_variable(variablesList[i],element_2[i])
                    else:
                        child_env.add_variable(variablesList,element_2)

                    self.stack.push(child_env.name)
                    self.control.append(child_env.name)
                    self.control += self.control_structures[element_1.id]

                # Tuple selection            
                elif(type(element_1) == tuple):
                    self.stack.push(element_1[element_2-1])
                # Y* combinator
                elif element_1 == "Y*":
                    temp = Eta(element_2.id, element_2.val, element_2.env) 
                    self.stack.push(temp)
                # Eta combinator
                elif isinstance(element_1, Eta):
                    temp = Lambda(element_1.id,element_1.val,element_1.env)
                    self.control.append("gamma")
                    self.control.append("gamma")
                    self.stack.push(element_2)
                    self.stack.push(element_1)
                    self.stack.push(temp)

                # Built-in functions
                elif(element_1 == "Order"):
                    order = len(element_2)
                    self.stack.push(order)
                elif(element_1 == "Print" or element_1 == "print"):
                    self.stack.push(element_2)
                    self.print_state = True
                elif(element_1 == "Conc"):
                    element_3 = self.stack.pop()
                    self.control.pop()
                    temp = element_2 + element_3
                    self.stack.push(temp)
                elif(element_1 == "Stern"):
                    self.stack.push(element_2[1:])

                elif(element_1 == "Stem"):
                    self.stack.push(element_2[0])

                elif(element_1 == "Isinteger"):
                    if(type(element_2) == int):
                        self.stack.push(True)
                    else:
                        self.stack.push(False)
                    
                elif(element_1 == "Istruthvalue"):
                    if(type(element_2) == bool):
                        self.stack.push(True)
                    else:
                        self.stack.push(False)

                elif(element_1 == "Isstring"):
                    if(type(element_2) == str):
                        self.stack.push(True)
                    else:
                        self.stack.push(False)

                elif(element_1 == "Istuple"):
                    if(type(element_2) == tuple):
                        self.stack.push(True)
                    else:
                        self.stack.push(False)

                elif(element_1 == "Isfunction"):
                    if(element_2 in self.built_in_functions):
                        return True
                    else:
                        False
                    
            # Handle environment switching
            elif type(element) == str and element[:2] == "e_" :
                stackSymbol = self.stack.pop()
                self.stack.pop()
                if(self.current_environment != 0):
                    for element in reversed(self.stack.items):
                        if(type(element) == str and element.startswith("e_")):
                            self.current_environment = int(element[2:])
                            break
                self.stack.push(stackSymbol)  

            # Handle binary operations
            elif element in self.binop:
                rand_1 = self.stack.pop()
                rand_2 = self.stack.pop()

                # Arithmetic and logical operations with error checking
                if element == "+":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1+rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("+","All operands for + must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("+","All operands for + must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("+","All operands for + must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break
                elif element == "-":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1-rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("-","All operands for - must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("-","All operands for - must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("-","All operands for - must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "*":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1*rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("*","All operands for * must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("*","All operands for * must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("*","All operands for * must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "/":
                    if rand_2 == 0:
                        self.errors.zero_division_error(rand_1)
                        break
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1/rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("/","All operands for / must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("/","All operands for / must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("/","All operands for / must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "**":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1**rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("**","All operands for ** must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("**","All operands for ** must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("**","All operands for ** must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "gr" or element == ">":
                    # self.stack.push(rand_1 > rand_2)
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1 > rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands(">","All operands for > must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands(">","All operands for > must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands(">","All operands for > must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "ge" or element == ">=":
                    # self.stack.push(rand_1 >= rand_2)
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1 >= rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands(">=","All operands for >= must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands(">=","All operands for >= must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands(">=","All operands for >= must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "ls" or element == "<":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1 < rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("<","All operands for < must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("<","All operands for < must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("<","All operands for < must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "le" or element == "<=":
                    if (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.stack.push(rand_1<=rand_2)
                    elif not (isinstance(rand_1,int) or isinstance(rand_1,float)) and (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("<=","All operands for <= must be integers. But a NON-INTEGER and a INTEGER is given")
                        break
                    elif (isinstance(rand_1,int) or isinstance(rand_1,float)) and not (isinstance(rand_2,int) or isinstance(rand_2,float)):
                        self.errors.unsupported_operands("<=","All operands for <= must be integers. But a INTEGER and a NON-INTEGER is given")
                        break
                    else:
                        self.errors.unsupported_operands("<=","All operands for <= must be integers. But a NON-INTEGER and a NON-INTEGER is given")
                        break

                elif element == "eq":
                    self.stack.push(rand_1 == rand_2)
                elif element == "ne":
                    self.stack.push(rand_1 != rand_2)

                elif element == "or":
                    if rand_1 == "true" or rand_1 == "false":
                        rand_1 = self.lookup(rand_1)
                        
                    if rand_2 == "true" or rand_2 == "false":
                        rand_2 = self.lookup(rand_2)

                    if isinstance(rand_1,bool) and isinstance(rand_2,bool):
                        self.stack.push(rand_1 or rand_2)
                    elif not isinstance(rand_1,bool) and isinstance(rand_2,bool):
                        self.errors.unsupported_operands("'or'","All operands for 'or' must be booleans. But a NON-BOOLEAN and a BOOLEAN is given")
                        break
                    elif isinstance(rand_1,bool) and not isinstance(rand_2,bool):
                        self.errors.unsupported_operands("'or'","All operands for 'or' must be booleans. But a BOOLEAN and a NON-BOOLEAN is given")
                        break
                    else:
                        self.errors.unsupported_operands("'or'","All operands for 'or' must be booleans. But a NON-BOOLEAN and a NON-BOOLEAN is given")
                        break

                elif element == "&":
                    if rand_1 == "true" or rand_1 == "false":
                        rand_1 = self.lookup(rand_1)
                        
                    if rand_2 == "true" or rand_2 == "false":
                        rand_2 = self.lookup(rand_2)                  

                    if isinstance(rand_1,bool) and isinstance(rand_2,bool):
                        self.stack.push(rand_1 and rand_2)
                    elif not isinstance(rand_1,bool) and isinstance(rand_2,bool):
                        self.errors.unsupported_operands("'and'","All operands for 'and' must be booleans. But a NON-BOOLEAN and a BOOLEAN is given")
                        break
                    elif isinstance(rand_1,bool) and not isinstance(rand_2,bool):
                        self.errors.unsupported_operands("'and'","All operands for 'and' must be booleans. But a BOOLEAN and a NON-BOOLEAN was given")
                        break
                    else:
                        self.errors.unsupported_operands("'and'","All operands for 'and' must be booleans. But a NON-BOOLEAN and a NON-BOOLEAN was given")
                        break
                
                elif element == "aug":
                    if rand_1 == "nil":
                        self.stack.push((rand_2))
                    elif type(rand_1) == tuple:
                        tlst = list(rand_1)
                        tlst.append(rand_2)
                        self.stack.push(tuple(tlst))
                    else:
                        tlst = [rand_1]
                        tlst.append(rand_2)
                        self.stack.push(tuple(tlst))

            # Handle unary operations (not, neg)
            elif element in self.unop:
                rand = self.stack.pop()
                if element == "not":
                    if rand == "true" or rand == "false":
                        rand = self.lookup(rand)
                    if isinstance(rand,bool):
                        self.stack.push(not rand)
                    else:
                        self.errors.unsupported_operands("'not'","Operand for 'not' is a boolean. But a NON-BOOLEAN was given")
                        break
                elif element == "neg":
                    if isinstance(rand,int):
                        self.stack.push(not rand)
                    else:
                        self.errors.unsupported_operands("'neg'","Operand for 'neg' is an integer. But a NON-INTEGER was given")
                        break


            # Handle if-else (beta)
            elif type(element) == str and element == "beta":
                B = self.stack.pop()
                deltaElse = self.control.pop()
                deltaThen = self.control.pop()
                if(B):
                    self.control += self.control_structures[deltaThen.id]
                else:
                    self.control += self.control_structures[deltaElse.id]


            # Handle tuple construction (Tau)
            elif type(element) == Tau :
                n = element.size
                tauList = []
                for i in range(n):
                    tauList.append(self.stack.pop())
                tauTuple = tuple(tauList)
                self.stack.push(tauTuple)


            # Handle Y* combinator
            elif type(element) == str and element == "Y*":
                self.stack.push(element)
            # Handle truth values
            elif type(element) == str and element == "true" or "false":
                self.stack.push(element)




    def print(self):
        # Prints the topmost string from the stack, with special characters escaped.
        if self.print_state:
            string = self.stack.pop()
            if type(string) == str:
                formatted_str = ""
                counter = 0
                while counter < len(string):
                    if string[counter] == "\\":
                        if string[counter+1] == "n":
                            formatted_str += "\n"
                            counter += 2
                        elif string[counter+1] == "t":
                            formatted_str += "\t"
                            counter += 2
                        elif string[counter+1] == "\\":
                            formatted_str += "\\"
                            counter += 2
                    else:
                        formatted_str += string[counter]
                        counter += 1
            else:
                formatted_str = string

            print(formatted_str)

            



        

