class Environment(object):
    # A class representing an environment for variable/function scope.

    def __init__(self, number, parent):
        # Initialize the environment with a unique name, empty variable dictionary,
        # empty list of children, and a reference to the parent environment.
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent = parent

    def add_child(self, child_env):
        # Add a child environment to this environment.
        # The child inherits all variables from the parent at creation.
        self.children.append(child_env)
        child_env.variables.update(self.variables)

    def add_variable(self, key, value):
        # Add a variable to the environment.
        self.variables[key] = value

    def __str__(self) -> str:
        # Return a string representation of the environment.
        return f"{self.name}[{self.variables}]"
    
    def __repr__(self) -> str:
        # Return a string representation for debugging.
        return f"Tau_{self.size}"