from CSComponents import Lambda, Delta, Tau
from copy import deepcopy

class ControlStructureBuilder:

# A class that builds control structures based on a given standardized tree (ST).
    #
    # Attributes:
    #   ST: The standardized syntax tree (Node object).
    #   control_structures: List of lists, each representing a control structure (delta).
    #   count: Counter to assign unique indices to control structures.


    # Initialize with the standardized tree.
    def __init__(self, SI_Tree):
        self.ST = SI_Tree
        self.control_structures = []
        self.count = 0

    # Public method to start pre-order traversal and build control structures.
    # Returns the list of control structures.
    def linerize(self):
        self.pre_order(self.ST, 0)
        return self.control_structures
    
    # Prints the control structures in a readable format.
    # Greek letters are used for gamma for clarity.
    def printCS(self):

            self.pre_order(self.ST, 0)
            cs = deepcopy(self.control_structures)
            for i in range(len(cs)): 
                for j in range(len(cs[i])):
                    if cs[i][j] == "gamma":
                        cs[i][j] = "\u03B3"
            for i in range(len(cs)):
                print(f"\u03B4_{i} : {cs[i]}")

    # Traverses the syntax tree in pre-order and builds the control structures.
    # Args:
    #   root: The current node being visited.
    #   index: The index of the current control structure (delta).
    def pre_order(self, root, index):

        # Ensure the control_structures list has enough sublists for the current index
        if len(self.control_structures) <= index:
            self.control_structures.append([])

        # Handle lambda nodes: create a Lambda object and add to control structures
        if root.data == "lambda":
            self.count += 1
            if root.children[0].data == ",":
                # Multiple parameters: collect all parameter names
                cs = Lambda(self.count)
                val = []
                for node in root.children[0].children:
                    val.append(node.data)
                cs.val = val
                self.control_structures[index].append(cs) 
            else:
                # Single parameter
                cs = Lambda(self.count,root.children[0].data)
                self.control_structures[index].append(cs)

            # Recursively process the body of the lambda
            for node in root.children[1:]:
                self.pre_order(node, self.count)

        # Handle conditional (->): create Delta objects for then/else branches and add beta
        elif root.data == "->":
            self.count += 1
            cs = Delta(self.count)
            self.control_structures[index].append(cs)
            self.pre_order(root.children[1], self.count)
            self.count += 1
            cs = Delta(self.count)
            self.control_structures[index].append(cs)
            self.pre_order(root.children[2], self.count)
            self.control_structures[index].append("beta")
            self.pre_order(root.children[0], index)
        
        # Handle tuple (tau): create a Tau object with the tuple size
        elif(root.data == "tau"):
            n = len(root.children)
            cs = Tau(n)
            self.control_structures[index].append(cs)
            for node in root.children:
                self.pre_order(node, index)
        
        # Handle all other nodes: add the node's data and process children
        else:
            self.control_structures[index].append(root.data)
            for node in root.children:
                self.pre_order(node, index)

