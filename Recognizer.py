class Recognizer:
    # Recognizer class to classify characters (digit, letter, operator, etc.)

    def __init__(self):
        # Initialize lists for different character classes.
        self.num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.punctuation = ['(', ')', ';', ',']
        self.letter_list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
            'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
        self.operator_list = [
            '+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', '!', '#', '%', '^',
            '_', '[', ']', '{', '}', '"', '`', '?'
        ]
        self.after_back_slash = ['t', 'n', '\\', '"']

    def is_digit(self, char):
        # Return True if the character is numeric.
        return char in self.num_list

    @staticmethod
    def is_space(char):
        # Return True if the char is a space or tab.
        return char == " " or char == "\t"

    def is_punctuation(self, char):
        # Return True if the char is a punctuation symbol.
        return char in self.punctuation

    def is_letter(self, char):
        # Return True if the character is a letter.
        return char in self.letter_list

    def is_operator(self, char):
        # Return True if the character is an operator symbol.
        return char in self.operator_list

    @staticmethod
    def is_eol(char):
        # Return True if the char is the end of line character.
        return char == "\n"

    @staticmethod
    def is_underscore(char):
        # Return True if the char is an underscore.
        return char == "_"

    @staticmethod
    def is_slash(char):
        # Return True if the char is a slash.
        return char == "/"

    @staticmethod
    def is_back_slash(char):
        # Return True if the char is a backslash.
        return char == "\u005c"

    def is_after_back_slash(self, char):
        # Return True if the char is a valid escape character after a backslash.
        return char in self.after_back_slash

    @staticmethod
    def is_double_quote(char):
        # Return True if the char is a double quote.
        return char == '"'

    @staticmethod
    def is_single_quote(char):
        # Return True if the char is a single quote.
        return char == "'"
    
    @staticmethod
    def is_ht(char):
        # Return True if the char is a horizontal tab.
        return char == '\t'