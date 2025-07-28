class ErrorHandler:
    # Handles errors during scanning, screening, parsing, and CSE machine execution.

    def __init__(self, reader=None, source_list=None):
        # Initialize the error handler with optional reader and source list.
        self.reader = reader
        self.error_status = False  # Flag to indicate if any error has occurred
        self.source_list = source_list
        self.error_list = []  # List to store error messages

    def syntax_error(self, index):
        # Handles syntax errors.
        # Args:
        #   index: The index in the source where the error occurred.
        # Adds a formatted error message to error_list.
        self.error_status = True
        line_no, line_index = self.reader.find_line(index)
        error_string = (
            f"\033[1;31mSyntax Error\033[0m in line {line_no} : {line_index} \n\t"
            f"{self.reader.get_line(line_no-1)[:line_index]}"
            f"\033[30;47m{self.reader.get_line(line_no-1)[line_index]}\033[0m"
            f"{self.reader.get_line(line_no-1)[line_index+1:-1]}"
        )
        self.error_list.append(error_string)

    def unrecognized_error(self, index):
        # Handles unrecognized character errors.
        # Args:
        #   index: The index in the source where the error occurred.
        # Adds a formatted error message to error_list.
        self.error_status = True
        line_no, line_index = self.reader.find_line(index)
        error_string = (
            f"\033[1;31mUnrecognized Character\033[0m in line {line_no} : {line_index} \n\t"
            f"{self.reader.get_line(line_no-1)[:line_index]}"
            f"\033[30;47m{self.reader.get_line(line_no-1)[line_index]}\033[0m"
            f"{self.reader.get_line(line_no-1)[line_index+1:-1]}"
        )
        self.error_list.append(error_string)

    def parse_error(self, error):
        # Handles errors during parsing.
        # Args:
        #   error: Error message string.
        # Adds a formatted error message to error_list.
        self.error_status = True
        error_string = f"\033[1;31mParsing Error\033[0m \n\t{error}\033[0m"
        self.error_list.append(error_string)

    def unsupported_operands(self, operation, types):
        # Handles errors for unsupported operand types in operations.
        # Args:
        #   operation: The operation name.
        #   types: Error string describing the type issue.
        # Adds a formatted error message to error_list.
        self.error_status = True
        error_string = f"\033[1;31mUnsupported Operand Types for {operation}\033[0m \n\t{types}\033[0m"
        self.error_list.append(error_string)

    def zero_division_error(self, operand1):
        # Handles division by zero errors.
        # Args:
        #   operand1: The operand being divided.
        # Adds a formatted error message to error_list.
        self.error_status = True
        error_string = f"\033[1;31mZero Divison Error\033[0m \n\tCannot divide {operand1} from 0\033[0m"
        self.error_list.append(error_string)
    
    def print(self):
        # Prints all errors in the error list if any errors have occurred.
        if self.error_status:
            for error in self.error_list:
                print(error)