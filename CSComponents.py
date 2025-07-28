class Lambda:
    """
    Represents a lambda function.

    Attributes:
        id (str): The ID of the lambda function.
        val (Any, optional): The value of the lambda function. Defaults to None.
        env (Any, optional): The environment of the lambda function. Defaults to None.
    """

    def __init__(self, id, val=None, env=None):
        self.id = id
        self.val = val
        self.env = env

    def __str__(self) -> str:
        """
        Returns a string representation of the lambda function.

        Returns:
            str: The string representation of the lambda function.
        """
        return f"\u03BB_{self.id}_{self.val}_{self.env}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the lambda function.

        Returns:
            str: The string representation of the lambda function.
        """
        return f"\u03BB_{self.id}_{self.val}_{self.env}"
 


class Eta:
    """A class representing Eta.

    Attributes:
        id (int): The ID of the Eta.
        val (Any, optional): The value of the Eta. Defaults to None.
        env (Any, optional): The environment of the Eta. Defaults to None.
    """

    def __init__(self, id, val=None, env=None):
        self.id = id
        self.val = val
        self.env = env

    def __str__(self) -> str:
        return f"\u03b7_{self.id}_{self.val}_{self.env}"
    
    def __repr__(self) -> str:
        return f"\u03b7_{self.id}_{self.val}_{self.env}"



class Delta:
    """A class representing a Delta object.

    Attributes:
        id (int): The id of the Delta object.

    """
    def __init__(self, id):
        self.id = id

    def __str__(self) -> str:
        return f"\u03B4_{self.id}"
    
    def __repr__(self) -> str:
        return f"\u03B4_{self.id}"


class Tau:
    """Create tau instacnces for the control sttructures
    """
    def __init__(self,size):
        self.size = size

    def __str__(self) -> str:
        return f"Tau_{self.size}"
    
    def __repr__(self) -> str:
        return f"Tau_{self.size}"
    

