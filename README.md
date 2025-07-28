# RPAL Interpreter

A Python-based interpreter for RPAL implementing lexical analysis, parsing, standardization, and execution through a Control Stack Environment (CSE) machine.

## Authors
- Amarasinghe A.A.D.H.S.: 220023U
- Sandiw K.B.I.: 220573E

## Project Overview

This interpreter processes RPAL programs through several phases:
1. **Lexical Analysis** - Tokenization of source code
2. **Syntax Analysis** - Abstract Syntax Tree (AST) generation
3. **Standardization** - Converting AST to Standardized Tree (ST)
4. **Control Structure Generation** - Converting ST to control structures
5. **Execution** - CSE machine evaluation

## Usage

### Direct Python Execution

```bash
# Basic execution (evaluate and run the program)
python3 myrpal.py <filename>

# Show Abstract Syntax Tree
python3 myrpal.py <filename> -ast

# Show Standardized Tree
python3 myrpal.py <filename> -st

# Show Control Structures
python3 myrpal.py <filename> -cs
```

### Using Makefile

```bash
# Run the program
make run file=<filename>

# Show Abstract Syntax Tree
make ast file=<filename>

# Show Standardized Tree
make st file=<filename>

# Show Control Structures
make cs file=<filename>
```

## Example

The project includes a sample RPAL program (`filename.txt`):

```rpal
let Sum(A) = Psum (A,Order A )
where rec Psum (T,N) = N eq 0 -> 0
 | Psum(T,N-1)+T N
in Print ( Sum (1,2,3,4,5) )
```

Running this program:
```bash
python3 myrpal.py filename.txt
# Output: 15
```

## Project Structure

```
├── myrpal.py           # Main entry point
├── Scanner.py          # Lexical analyzer
├── Parser.py           # Syntax analyzer and AST builder
├── ControlStructures.py # Control structure generator
├── CSEMachine.py       # CSE machine for execution
├── Node.py             # Tree node implementation
├── Token.py            # Token class
├── ErrorHandler.py     # Error handling
├── Reader.py           # File reading utilities
├── Recognizer.py       # Token recognition
├── Stack.py            # Stack implementation
├── Environment.py      # Environment management
├── CSComponents.py     # CSE machine components
├── Makefile            # Build automation
├── filename.txt        # Sample RPAL program
└── test_simple.txt     # Simple test case
```

## Components

- **Scanner**: Performs lexical analysis, converting source code into tokens
- **Parser**: Builds Abstract Syntax Tree from tokens
- **ControlStructures**: Converts standardized tree to control structures for execution
- **CSEMachine**: Control Stack Environment machine that executes the control structures
- **ErrorHandler**: Manages and reports compilation and runtime errors

## RPAL Language Features

This interpreter supports standard RPAL constructs including:
- Function definitions and applications
- Recursive functions
- Conditional expressions
- Tuples and tuple operations
- Arithmetic and logical operations
- Let-where expressions
- Lambda expressions

## Development

This project was developed as part of CS 3513 - Programming Languages coursework, implementing a complete interpreter for the RPAL functional programming language.
