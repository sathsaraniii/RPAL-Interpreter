# Default Makefile for RPAL Interpreter

.PHONY: run ast st cs


# Run the interpreter normally (evaluate)
run:
	python3 myrpal.py $(file)

# Print Abstract Syntax Tree
ast:
	python3 myrpal.py $(file) -ast

# Print Standardized Tree
st:
	python3 myrpal.py $(file) -st

# Print Control Structures
cs:
	python3 myrpal.py $(file) -cs

