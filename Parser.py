from Token import Token
from Node import Node
import copy

class Parser:

    # Initialize the parser with a screener (Scanner object)
    def __init__(self,screener):
        self.screener = screener
        self.token_list = self.screener.get_tokens() 
        self.next_token = Token(None, None)
        self.index = 0
        self.stack = []
        self.ST = None
        self.pre_ordered = []
        self.errors = screener.errors

    # Print the Abstract Syntax Tree (AST)
    def printAST(self):

        tree = self.stack[0]
        def traverse(root, n):
            print("."*n + root.data)

            if root.children:
                for node in root.children:
                    traverse(node, n+1)

        traverse(tree, 0)

    # Print the Standardized Tree (ST)
    def printST(self):

        if self.ST == None:
            self.standardize()
        tree = self.ST
        def traverse(root, n):
            print("."*n + root.data)

            if root.children:
                for node in root.children:
                    traverse(node, n+1)

        traverse(tree, 0)

    # Build the AST by creating a node with n children
    def build_tree(self,transduction, n):

        node = Node(transduction)
        if len(self.stack) >= n:
            for i in range(n):
                node.add_child(self.stack.pop())
            self.stack.append(node)
        else:
            self.errors.parse_error(f"Stack size {len(self.stack)} is less than {n} , cannot create node {self.next_token}")

    # Read the next token and build a leaf node if it's a value
    def read(self, token):

        tags = ["OPERATOR", "PUNCTUATION"]
        if (token.key != 'KEYWORD') and (token.key not in tags):
            if token.key == 'IDENTIFIER':
                self.build_tree(f"<ID:{token.val}>", 0)

            if token.key == 'INTEGER':
                self.build_tree(f"<INT:{token.val}>", 0)

            if token.key == 'STRING':
                self.build_tree(f"<STR:{token.val}>", 0)
        self.index += 1
        self.next_token = self.token_list[self.index]

    # Main parse method: starts parsing from the start symbol
    def parse(self):

        self.token_list.append(Token("$", "$"))
        self.index = 0
        self.next_token = self.token_list[self.index]
        self.E()
        if self.next_token.key == "$":
            pass

# Grammar rule methods (E, Ew, T, Ta, etc.) follow below.
# Each method implements a non-terminal in the RPAL grammar.
# They recursively call each other and build the AST using build_tree.

    def E(self):
        """
        E   ->  'let' D 'in' E => 'let'
            ->  'fn' Vb+ '.' E => 'lambda'
            ->  Ew;
        """

        if self.next_token.val == "let":
            self.read(self.next_token)
            self.D()

            if self.next_token.val == "in":
                self.read(self.next_token)
                self.E()
                self.build_tree("let", 2)

            else:
                self.errors.parse_error(f"Got '{self.next_token.val}' expected 'in' ")

        elif self.next_token.val == "fn":
            self.read(self.next_token)

            self.Vb()
            n = 1

            while self.next_token.key == "IDENTIFIER" or (self.next_token.key == "PUNCTUATION" and self.next_token.key == "("):
                self.Vb()
                n += 1

            if self.next_token.key == "OPERATOR" and self.next_token.val == ".":
                self.read(self.next_token)
                self.E()
                self.build_tree("lambda", n+1)

            else:
                self.errors.parse_error("'.' expected")

        else:
            self.Ew()


    def Ew(self):
        """
        Ew  ->  T 'where' Dr => 'where'
            ->  T
        """
        self.T()

        if self.next_token.val == "where":
            self.read(self.next_token)
            self.Dr()
            self.build_tree("where", 2)


    def T(self):
        """
        T   ->  Ta(',' Ta )+ => 'tau'
            ->  Ta ;
        """
        self.Ta()

        n = 1
        while self.next_token.key == "PUNCTUATION" and self.next_token.val == ",":
            self.read(self.next_token)
            self.Ta()
            n += 1

        if n > 1:
            self.build_tree('tau', n)


    def Ta(self):
        """
        Ta  ->  Ta 'aug' Tc => 'aug'
            ->  Tc
        """
        self.Tc()

        while self.next_token.val == "aug":
            self.read(self.next_token)
            self.Tc()
            self.build_tree("aug", 2)


    def Tc(self):
        """
        Tc  ->  B '->' Tc '|' Tc => '->'
            ->  B;
        """
        self.B()

        if self.next_token.val == "->":
            self.read(self.next_token)
            self.Tc()

            if self.next_token.key == "OPERATOR" and self.next_token.val == "|":
                self.read(self.next_token)
                self.Tc()
                self.build_tree("->", 3)
            else:
                self.errors.parse_error("Error: '|' expected")
                # print("Error: '|' expected")


    def B(self):
        """
        B   ->  B 'or' Bt => 'or'
            ->  Bt
        """ 
        self.Bt()

        while self.next_token.val == "or":
            self.read(self.next_token)
            self.Bt()
            self.build_tree("or", 2)


    def Bt(self):
        """
        Bt  ->  Bt '&' Bs => '&'
            ->  Bs
        """
        self.Bs()

        while self.next_token.val == "&":
            self.read(self.next_token)
            self.Bs()
            self.build_tree("&", 2)


    def Bs(self):
        """
        Bs  ->  'not' Bp => 'not'
            ->  Bp
        """
        if self.next_token.val == "not":
            self.read(self.next_token)
            self.Bp()
            self.build_tree("not", 1)

        else:
            self.Bp()


    def Bp(self):
        """
        Bp  ->  A ('gr' | '>' ) A => 'gr'
            ->  A ('ge' | '>=') A => 'ge'
            ->  A ('ls' | '<') A => 'ls'
            ->  A ('le' | '<=') A => 'le'
            ->  A 'eq' A => 'eq'
            ->  A 'ne' A => 'ne'
            ->  A
        """
        self.A()

        if self.next_token.val in ("gr", ">"):
            self.read(self.next_token)
            self.A()
            self.build_tree("gr", 2)

        elif self.next_token.val in ("ge", ">="):
            self.read(self.next_token)
            self.A()
            self.build_tree("ge", 2)

        elif self.next_token.val in ("ls", "<"):
            self.read(self.next_token)
            self.A()
            self.build_tree("ls", 2)

        elif self.next_token.val in ("le", "<="):
            self.read(self.next_token)
            self.A()
            self.build_tree("le", 2)

        elif self.next_token.val == "eq":
            self.read(self.next_token)
            self.A()
            self.build_tree("eq", 2)

        elif self.next_token.val == "ne":
            self.read(self.next_token)
            self.A()
            self.build_tree("ne", 2)

        else:
            pass


    def A(self):
        """
        A   ->  A '+' At => '+'
            ->  A '-' At => '-'
            ->  '+' At
            ->  '-' At => 'neg'
            ->  At
        """
        if self.next_token.key == "OPERATOR" and self.next_token.val == "+":
            self.read(self.next_token)
            self.At()

        elif self.next_token.key == "OPERATOR" and self.next_token.val == "-":
            self.read(self.next_token)
            self.At()
            self.build_tree("neg", 1)  # check num

        else:
            self.At()

            while self.next_token.key == "OPERATOR" and self.next_token.val in ("+", "-"):
                if self.next_token.val == "+":
                    self.read(self.next_token)
                    self.At()
                    self.build_tree("+", 2)  # check num

                else:
                    self.read(self.next_token)
                    self.At()
                    self.build_tree("-", 2)  # check num


    def At(self):
        """
        At  ->  At '*' Af => '*'
            ->  At '/' Af => '/'
            -> Af
        """
        self.Af()

        while self.next_token.key == "OPERATOR" and self.next_token.val in ("*", "/"):
            if self.next_token.val == "*":
                self.read(self.next_token)
                self.Af()
                self.build_tree("*", 2)

            else:
                self.read(self.next_token)
                self.Af()
                self.build_tree("/", 2)


    def Af(self):
        """
        Af  ->  Ap '**' Af => '**'
            ->  Ap
        """
        self.Ap()

        if self.next_token.val == "**":
            self.read(self.next_token)
            self.Af()
            self.build_tree("**", 2)  


    def Ap(self):
        """
        Ap  ->  Ap ’@’ ’<IDENTIFIER>’ R => ’@
            ->  R
        """
        self.R()

        while self.next_token.key == "OPERATOR" and self.next_token.val == "@":
            self.read(self.next_token)

            if self.next_token.key == "IDENTIFIER":
                self.read(self.next_token)
                self.R()
                self.build_tree("@", 3)

            else:
                self.errors.parse_error("Identifier expected")


    def R(self):
        """
        R   ->  R Rn => ’gamma’
            ->  Rn
        """
        self.Rn()

        while ((self.next_token.key in ("IDENTIFIER", "INTEGER", "STRING")) or (self.next_token.val in ("true", "false", "dummy", "nil", "("))):
            self.Rn()
            self.build_tree("gamma", 2)


    def Rn(self):
        """
        Rn  ->  '<IDENTIFIER>'
            ->  '<INTEGER>'
            ->  '<STRING>'
            ->  'true' => 'true'
            ->  'false' => 'false'
            ->  'nil' => 'nil'
            ->  '(' E ')'
            ->  'dummy' => 'dummy'
        """
        if self.next_token.val == "true":
            self.read(self.next_token)
            self.build_tree("true", 0) # check the numbers in build_tree

        elif self.next_token.val == "false":
            self.read(self.next_token)
            self.build_tree("false", 0)  # check the numbers in build_tree

        elif self.next_token.val == "nil":
            self.read(self.next_token)
            self.build_tree("nil", 0)  # check the numbers in build_tree

        elif self.next_token.val == "dummy":
            self.read(self.next_token)
            self.build_tree("dummy", 0)  # check the numbers in build_tree

        elif self.next_token.key in ("IDENTIFIER", "INTEGER", "STRING"):
            self.read(self.next_token)

        elif self.next_token.val == "(":
            self.read(self.next_token)

            self.E()

            if self.next_token.val != ")":
                self.errors.parse_error("Expected a matching )")

            else:
                self.read(self.next_token)

        else:
            self.errors.parse_error("Error in Rn")


    def D(self):
        """
        D   ->  Da 'within' D  => 'within'
            ->  Da
        """
        self.Da()

        if self.next_token.val == "within":
            self.read(self.next_token)
            self.D()
            self.build_tree("within", 2)  # check num


    def Da(self):
        """
        Da  ->  Dr ('and' Dr)+  => 'and'
            ->  Dr
        """
        self.Dr()

        n = 1
        while self.next_token.val == "and":
            self.read(self.next_token)
            self.Dr()
            n += 1

        if n > 1:
            self.build_tree("and", n)


    def Dr(self):
        """
        Dr  ->  'rec' Db  => 'rec'
            ->  Db
        """
        if self.next_token.val == "rec":
            self.read(self.next_token)
            self.Db()
            self.build_tree("rec", 1)  # check num

        else:
            self.Db()


    def Db(self):
        """
        Db  ->  Vl '=' E   =>  '='
            ->  '<IDENTIFIER>' Vb+ '=' E  => 'fcn_form'
            ->  '(' D ')'
        """

        if self.next_token.key == "IDENTIFIER":
            if len(self.token_list) > self.index+1:
                
#    Ambiguity note:
#       When parsing Db, both Vl and Vb+ can start with <IDENTIFIER>.
#       Therefore, we cannot decide the correct production using only next_token (LL(1)).
#       We must look ahead to the token after next_token (LL(2)) to resolve the ambiguity.

                if self.token_list[self.index+1].val == "=" or self.token_list[self.index+1].val == ",": 
                    self.Vl()
                    self.read(self.next_token)
                    self.E()
                    self.build_tree("=", 2)


                elif self.token_list[self.index+1].key == "IDENTIFIER" or self.token_list[self.index+1].val == "(":
                    self.read(self.next_token)
                    self.Vb()
                    n = 1

                    while self.next_token.key == "IDENTIFIER" or self.next_token.val == "(":
                        self.Vb()
                        n += 1
                    if self.next_token.val == "=":
                        self.read(self.next_token)
                        self.E()
                        self.build_tree("fcn_form", n+2)

                    else:
                        self.errors.parse_error("'=' expected")

                else:
                    self.errors.parse_error("'=' or an identifier expected")

        elif self.next_token.val == "(":
            self.read(self.next_token)
            self.D()

            if self.next_token.val == ")":
                self.read(self.next_token)

        else:
            pass


    def Vb(self):
        """
        Vb  ->  '<IDENTIFIER>'
            ->  '(' Vl ')'
            ->  '(' ')'  => '()'
        """
        if self.next_token.key == "IDENTIFIER":
            self.read(self.next_token)

        elif self.next_token.val == "(":
            self.read(self.next_token)

            isvl = False

            if self.next_token.key == "IDENTIFIER" :
                self.Vl()
                isvl = True

            if self.next_token.val == ")":
                self.read(self.next_token)

                if not isvl:
                    self.build_tree("()", 0)  # check num

            else:
                self.errors.parse_error("')' expected")

        else:
            self.errors.parse_error("'(' or an identifier expected")


    def Vl(self):
        """
        Vl -> '<IDENTIFIER>' list ','  => ','?
        """
        n = 0
        while self.next_token.key == "IDENTIFIER":
            self.read(self.next_token)
            n += 1

            if self.next_token.val == ",":
                self.read(self.next_token)
            else:
                break
        if n > 1:
            self.build_tree(",", n)


    def standardize(self):
        self.ST = copy.deepcopy(self.stack[0])
        self.ST = self.buildST(self.ST)


    def printNode(self, node):
        tree = node
        def traverse(root, n):
            print("."*n + root.data)

            if root.children:
                for node in root.children:
                    traverse(node, n+1)
        traverse(tree, 0)


    def buildST(self, node):
        for child in node.children:
            self.buildST(child)
        

        if node.data == "let" and node.children[0].data == "=":
            #   let              gamma              
            #   / \               / \                
            #  =   P    =>   lambda   E            
            # / \             /  \              
            # X   E          X    P              

            eq_node = node.children[0]
            p_node = node.children[1]

            node.children[1] = eq_node.children[1]      # P -> E
            node.children[0].children[1] = p_node       # E -> P
            node.children[0].data = "lambda"            # = -> lambda
            node.data = "gamma"                         # let -> gamma

        elif node.data == "where" and node.children[1].data == "=":
            #  where              gamma              
            #   / \               /  \                
            #  P   =    =>    lambda  E          
            #     / \          /  \                   	 
            #    X   E        X    P                   

           
            child_0 = node.children[0] #p
            child_1 = node.children[1] #=

            node.children[0] = child_1.children[1]
            node.children[1].children[1] = child_0
            node.children[1].data = "lambda"
            node.children[0], node.children[1] = node.children[1], node.children[0]
            node.data = "gamma"

        elif node.data == "fcn_form":
            # fcn_form          	        =
            # /   |  \         		   / \
            # P   V+   E      =>      P   +lambda
            #                                /  \
            #                                V   .E 
            e_node = node.children.pop()

            current_node = node
            for i in range(len(node.children) - 1):
                lambda_node = Node("lambda")                    # Creating lambda node
                lamnbda_left_child = node.children.pop(1)       # Taking the first V in the children list
                lambda_node.add_child_end(lamnbda_left_child)       # Adding the firt V as the left child of the lambda node
                current_node.add_child_end(lambda_node)             # Add the lambda node as the second children of the current_node
                current_node = lambda_node                      # Traverse one level down using lambda node

            current_node.add_child_end(e_node)                      # Add e_node as the second child of the last lambda_node
            node.data = "="                                     # fcn_form -> =




        elif node.data == "lambda" and len(node.children) > 2:
            #  lambda    =>    ++lambda  
            #  /   \             /   \   
            # V++   E           V    .E 
            
            e_node = node.children.pop()
            current_node = node
            for i in range(len(node.children) - 1):
                lambda_node = Node("lambda")                    # Create a lambda node
                child = node.children.pop(1)                    # Pop the second V out from the node
                lambda_node.add_child_end(child)                # Add the second V to the lambda node as a child
                current_node.add_child_end(lambda_node)         # Add the lambda node as the child node to the current_node
                current_node = lambda_node                      # Make the lambda node the current node

            current_node.add_child_end(e_node)                  # Add the e_node to the final current_node(lambda node)



        elif node.data == "within" and node.children[0].data == node.children[1].data == "=":
            # 	within    	    =>        	  =     
            #     /     \              		/   \    
            #    =       =         	 	  X2  gamma 
            #   / \     /  \             		  /    \  
            # X1  E1   X2   E2       		 lambda     E1 
            #                               /  \       
            #                              X1   E2 

            
            x2_node = node.children[1].children[0]
            e1_node = node.children[0].children[1]
            x1_node = node.children[0].children[0]
            e2_node = node.children[1].children[1]
            gamma_node = Node("gamma")

            gamma_node.add_child_end(Node("lambda"))            # Add a lambda node to the gamma node
            gamma_node.add_child_end(e1_node)                   # Add e1_node to the gamma node
            gamma_node.children[0].add_child_end(x1_node)           # Add x1_node to the lambda_node
            gamma_node.children[0].add_child_end(e2_node)           # Add e2_node to the lambda_node

            node.children[0] = x2_node                          # Make x2_node the first child of the within node
            node.children[1] = gamma_node                       # Make gamma_node the second child of the within node

            node.data = "="                                     # within -> =

        elif node.data == "@":
            #    @        =>      gamma
            #  / | \            	/   \
            # E1 N  E2         gamma   E2
            #                  /  \
            #                 N    E1

            e1_node = node.children.pop(0)
            n_node = node.children[0]

            gamma_node = Node("gamma")                  # Creating a gamma node
            gamma_node.add_child_end(n_node)            # Add n_node to the gamma node
            gamma_node.add_child_end(e1_node)           # Add e1_node to the gamma node

            node.children[0] = gamma_node               # Make the first child of @ node the gamma node
            node.data = "gamma"                         # @ -> gamma


        elif node.data == "and":
            # and     =>       =       
            #  |             	/ \      
            # =++            ,  tau    
            # / \            |    |     
            # X   E          X++   E++   

            child_0 = Node(",")
            child_1 = Node("tau")

            for child in node.children:
                child_0.add_child_end(child.children[0])
                child_1.add_child_end(child.children[1])

            node.children.clear()

            node.add_child_end(child_0)
            node.add_child_end(child_1)

            node.data = "="





        elif node.data == "rec":
            #    rec     =>           =
            #     |                  / \
            #     =                 X   gamma
            #    / \                    /   \
            #   X   E           	  Ystar  lambda
            #                               /  \
            #                              X    E
            

            temp = node.children.pop()
            temp.data = "lambda"

            gammaNode = Node("gamma")
            gammaNode.add_child_end(Node("Y*"))
            gammaNode.add_child_end(temp)

            node.add_child_end(temp.children[0])
            node.add_child_end(gammaNode)

            node.data = "="

        return node
    

    def pre_order(self):
        if self.ST == None:
            self.standardize()
        self.printPreOrder(self.ST)
        return self.pre_ordered

    # Helper method for pre-order traversal of the standardized tree (ST)
    # Appends each node's data to self.pre_ordered in pre-order sequence
    def printPreOrder(self, node):

        # Base case: if the node is None, return
        if node is None:
            return
        
        # Add the current node's data to the pre_ordered list
        self.pre_ordered.append(node.data)

        # Recursively traverse all children in order
        for i in range(len(node.children)):
            self.printPreOrder(node.children[i])

   