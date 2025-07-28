
class Token:
    # Token class to create token instances for the parser and other modules.
    
    def __init__(self, typeClass, value):
        # Initialize a Token with its type and value.
        # If the value is a reserved keyword, set key to "KEYWORD".
        self.keywords = ['let','in','fn','where','aug','or','not','gr','ge','ls','le','eq','ne','true','false','nil','dummy','within','and','rec']
        
        if value in self.keywords:
            self.key = "KEYWORD"
        else:
            self.key = typeClass    # For non-keywords, use the provided typeClass as the key.
        self.val = value

    def __str__(self):
        return f"(<{self.key}>, {self.val})"    # String representation for printing.

    
    def __repr__(self):
        return f"(<{self.key}>, {self.val})"    # Representation for debugging and lists.
