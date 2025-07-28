class Reader:
    # Reader class to read the source file and provide utility methods for line/character mapping.

    def __init__(self, filename):
        # Initialize the Reader with the given filename.
        self.file = filename
        self.str = ""      # Entire file content as a single string
        self.lines = []    # List of lines in the file
        try:
            source = open(filename, 'r')
            self.lines = source.readlines()
            self.lines[-1] += " "  # Add a space to the last line for easier parsing
            for line in self.lines:
                self.str += line
        except:
            # Print an error message if the file cannot be opened.
            print(f"\033[1;31mUnknown File\033[0m \n\t \033[30;47m{filename}\033[0m")
        
    def read_whole(self):
        # Return the entire file content as a single string.
        return self.str
    
    def find_line(self, index):
        # Given a character index, find the corresponding line number and line index.
        line = 0
        cummutative_index = len(self.lines[line])
        while(index > cummutative_index):
            line += 1
            cummutative_index += len(self.lines[line])
        return line+1, index-cummutative_index + len(self.lines[line])
    
    def read_lines(self):
        # Return the lines of the file as a list.
        return self.lines

    def get_line(self, line_number):
        # Given the line number, return the corresponding line.
        return self.lines[line_number]