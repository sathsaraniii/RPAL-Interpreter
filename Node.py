class Node:
    # Node class to create tree nodes for parser trees.
    
    def __init__(self, data):
        # Initialize a Node with its data and an empty list of children.
        self.data = data
        self.children = []

    def add_child(self, child):
        # Add a child node to the beginning of the children list.
        self.children.insert(0, child)

    def add_child_end(self, child):
        # Add a child node to the end of the children list.
        self.children.append(child)

    def remove_child(self, child):
        # Remove a child node if it exists in the children list.
        if child in self.children:
            self.children.remove(child)
        else:
            print("Child not found")

    def __str__(self):
        return f" ({self.data} , {self.children}) "     # String representation for printing.

    
    def __repr__(self):
        return f" ({self.data} , {self.children}) "     # Representation for debugging and lists.
