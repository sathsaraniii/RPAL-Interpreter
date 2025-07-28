from ErrorHandler import ErrorHandler
from Reader import Reader
from Recognizer import Recognizer
from Token import Token

#    Scanner class for lexical analysis.
#    Reads the source code and converts it into a list of tokens for the parser.
class Scanner:

    def __init__(self, file_name):

        #Initialization
        self.reader = Reader(file_name)
        self.source_list = self.reader.read_whole()
        self.token_list = []
        self.current_index = 0
        self.last_index = len(self.source_list) -1
        self.recognizer = Recognizer()
        self.errors = ErrorHandler(self.reader,self.source_list)
        # Token type names
        self.id_name = "IDENTIFIER"
        self.int_name = "INTEGER"
        self.operator_name = "OPERATOR"
        self.string_name = "STRING"
        self.delete_name = "DELETE"
        self.punctuation_name = "PUNCTUATION"
        self.screened = False # Flag to indicate if the tokens have been screened

#   Main tokenization loop.
#   Reads characters from source_list and delegates to handlers based on character type.
    def tokenize(self):

        while self.current_index <= self.last_index:
            # Handle identifiers (variables, keywords)
            if self.recognizer.is_letter((self.source_list[self.current_index])):
                self.handle_identifier()
            # Handle integers (numbers)
            elif self.recognizer.is_digit((self.source_list[self.current_index])):
                self.handle_integer()
            # Handle strings (enclosed in single quotes)
            elif self.recognizer.is_single_quote(self.source_list[self.current_index]):
                if self.current_index != self.last_index:
                    self.handle_string()
                else:
                    self.errors.syntax_error(self.current_index)
                    self.current_index += 1
            # Handle comments (//)
            elif self.recognizer.is_slash(self.source_list[self.current_index]):
                self.current_index += 1
                if self.recognizer.is_slash(self.source_list[self.current_index]):
                    self.current_index += 1
                    self.handle_comment()
                else:
                    self.current_index -= 1
                    self.handle_operator()
            # Handle operators (arithmetic and logical)
            elif self.recognizer.is_operator((self.source_list[self.current_index])):
                self.handle_operator()
            # Handle spaces (whitespace, tabs, newlines)
            elif self.recognizer.is_space(self.source_list[self.current_index]) or self.recognizer.is_eol(
                    self.source_list[self.current_index]) or self.recognizer.is_ht(self.source_list[self.current_index]):
                self.handle_space()
            # Handle punctuation (commas, semicolons etc.)
            elif self.recognizer.is_punctuation(self.source_list[self.current_index]):
                self.handle_punctuation()
            # Handle unrecognized characters
            else:
                self.current_index += 1
                self.errors.unrecognized_error(self.current_index)

            if self.current_index >= self.last_index:
                break

#   Handles identifier tokens (variables, keywords).
#   Reads consecutive letters, digits, or underscores and adds the identifier to token_list.
    def handle_identifier(self):
 
        identifier_value = self.source_list[self.current_index]
        self.current_index += 1
        while self.current_index <= self.last_index and (self.recognizer.is_letter(self.source_list[self.current_index]) or
                                                      self.recognizer.is_digit(self.source_list[self.current_index]) or
                                                      self.recognizer.is_underscore(self.source_list[self.current_index])):
            identifier_value += self.source_list[self.current_index]
            self.current_index += 1
            if self.current_index == self.last_index:
                identifier_value += self.source_list[self.current_index]
                self.token_list.append((self.id_name, identifier_value))
                return
        else:
            self.token_list.append((self.id_name, identifier_value))

#   Handles integer tokens.
#   Reads consecutive digits and adds the integer to token_list.
    def handle_integer(self):

        integer_value = self.source_list[self.current_index]
        self.current_index += 1
        while self.current_index <= self.last_index and self.recognizer.is_digit(self.source_list[self.current_index]):
            integer_value += self.source_list[self.current_index]
            self.current_index += 1
            if self.current_index == self.last_index:
                integer_value += self.source_list[self.current_index]
                self.token_list.append((self.int_name, integer_value))
                return
        
        else:
            self.token_list.append((self.int_name, integer_value))

#   Handles operator tokens (e.g., +, -, *, /, etc.).
#   Reads consecutive operator characters and adds to token_list.
    def handle_operator(self):

        operator_value = self.source_list[self.current_index]
        self.current_index += 1
        while self.current_index <= self.last_index and self.recognizer.is_operator(
                self.source_list[self.current_index]) and self.current_index <= self.last_index:
            operator_value += self.source_list[self.current_index]
            self.current_index += 1
            if self.current_index == self.last_index:
                operator_value += self.source_list[self.current_index]
                break
        else:
            self.token_list.append((self.operator_name, operator_value))

#   Handles comment tokens.
#   Reads until the end of the line and adds the comment to token_list as DELETE type.
    def handle_comment(self):

        comment_value = "//"
        while self.current_index <= self.last_index and (
                self.recognizer.is_double_quote(self.source_list[self.current_index]) or
                self.recognizer.is_punctuation(self.source_list[self.current_index]) or
                self.recognizer.is_back_slash(self.source_list[self.current_index]) or
                self.recognizer.is_space(self.source_list[self.current_index]) or
                self.recognizer.is_letter(self.source_list[self.current_index]) or
                self.recognizer.is_digit(self.source_list[self.current_index]) or
                self.recognizer.is_operator(self.source_list[self.current_index]) or
                self.recognizer.is_eol(self.source_list[self.current_index])):

            comment_value += self.source_list[self.current_index]
            self.current_index += 1

            if self.recognizer.is_eol(self.source_list[self.current_index - 1]):
                break

            if self.current_index == self.last_index and self.recognizer.is_eol(self.source_list[self.current_index]):
                comment_value += self.source_list[self.current_index]
                break

        self.token_list.append((self.delete_name, comment_value))

#    Handles whitespace tokens (spaces, tabs, newlines).
#    Groups consecutive whitespace and adds to token_list as DELETE type.
    def handle_space(self):
 
        if self.current_index > self.last_index:
            return
        space_value = self.source_list[self.current_index]
        self.current_index += 1
        while self.current_index <= self.last_index and (self.recognizer.is_space(self.source_list[self.current_index]) or 
                                                    self.recognizer.is_eol(self.source_list[self.current_index]) or
                                                    self.recognizer.is_ht(self.source_list[self.current_index])):
            space_value += self.source_list[self.current_index]
            self.current_index += 1
            if self.current_index == self.last_index:
                space_value += self.source_list[self.current_index]
                return
        self.token_list.append((self.delete_name, space_value))

#   Handles string tokens (enclosed in single quotes).
#   Reads until the closing quote and adds the string to token_list.
#   Handles escape sequences and errors for unterminated strings.
    def handle_string(self):

        string_value = ""
        self.current_index += 1

        while self.current_index <= self.last_index and (self.recognizer.is_letter(self.source_list[self.current_index]) or
                                                      self.recognizer.is_digit(self.source_list[self.current_index]) or
                                                      self.recognizer.is_operator(self.source_list[self.current_index]) or
                                                      self.recognizer.is_back_slash(
                                                          self.source_list[self.current_index]) or
                                                      self.recognizer.is_punctuation(
                                                          self.source_list[self.current_index]) or
                                                      self.recognizer.is_space(self.source_list[self.current_index]) or
                                                      self.recognizer.is_eol(self.source_list[self.current_index]) or
                                                      self.recognizer.is_ht(self.source_list[self.current_index]) or
                                                      self.recognizer.is_single_quote(self.source_list[self.current_index])
                                                      ):
            
            # Handle closing quote and escape sequences
            if self.current_index == self.last_index-1:
                if self.recognizer.is_single_quote(self.source_list[self.current_index]):
                    self.current_index += 1
                    if self.recognizer.is_single_quote(self.source_list[self.current_index]):
                        string_value += self.source_list[self.current_index]
                        self.token_list.append((self.string_name, string_value))
                        return
                    else:
                        self.errors.syntax_error(self.current_index)
                        return
                else:
                    self.current_index += 1
                    self.errors.syntax_error(self.current_index)
                    return


            if self.recognizer.is_eol(self.source_list[self.current_index]):
                self.errors.syntax_error(self.current_index-1)
                return

            if self.recognizer.is_back_slash(self.source_list[self.current_index]):
                string_value += self.source_list[self.current_index]
                self.current_index += 1

                if self.current_index <= self.last_index and self.recognizer.is_after_back_slash(
                        self.source_list[self.current_index]):
                    string_value += self.source_list[self.current_index]
                    self.current_index += 1

            if self.recognizer.is_single_quote(self.source_list[self.current_index]):
                self.current_index += 1
                self.token_list.append((self.string_name, string_value))
                return
                

            string_value += self.source_list[self.current_index]
            self.current_index += 1

#   Handles punctuation tokens (e.g., commas, semicolons).
#   Adds the punctuation to token_list.
    def handle_punctuation(self):
 
        self.token_list.append((self.punctuation_name, self.source_list[self.current_index]))
        self.current_index += 1
        return

#   Screening process for the created tokens.
#   Removes tokens marked as DELETE (comments, whitespace).   
    def screen(self):

        self.screened = True
        new_tokens = []
        for token in self.token_list:
            if token[0] != self.delete_name:
                new_tokens.append(token)

        self.token_list = new_tokens

#   Prints the token list or error messages.
#   Shows scanning status. 
    def print(self, print_token = True):

        if self.errors.error_status:
            self.errors.print()
            print(f"\033[1;41m Scanning {'and Screening ' if self.screened else ''}exited with {len(self.errors.error_list)} error{'s' if len(self.errors.error_list) >1 else ''}. \033[0m")
        else:
            if print_token:
                for i in self.token_list:
                    print(i)
            print(f"\033[1;42m Scanning {'and Screening ' if self.screened else ''}finished sucessfullly. \033[0m")

#   Returns the scanned and screened token list as Token objects.
#   Triggers tokenization and screening if not already done.
#   return: list of Token objects
    def get_tokens(self):

        self.tokenize()
        self.screen()
        tokens_list = []
        for i in self.token_list:
            tokens_list.append(Token(i[0],i[1]))
        return tokens_list

