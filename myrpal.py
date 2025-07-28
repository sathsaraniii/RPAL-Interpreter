#!/usr/bin/env python

""" CS 3513 - Programming Languages: Programming Project 01 """""

__author__ = "Amarasinghe A.A.D.H.S.: 220023U, Sandiw K.B.I.: 220573E"
__version__ = "0.0.1"
__status__ = "Draft"


import sys

from Parser import Parser
from Scanner import Scanner
from ControlStructures import ControlStructureBuilder
from CSEMachine import CSEMachine

# Parse command-line arguments
# AST, ST, CS: Flags to determine which output mode to use
file_name = sys.argv[1]
AST = True if len(sys.argv) == 3 and sys.argv[2] == "-ast" else False
ST = True if len(sys.argv) == 3 and sys.argv[2] == "-st" else False
CS = True if len(sys.argv) == 3 and sys.argv[2] == "-cs" else False

# Initialize parser and parse input
p = Parser(Scanner(file_name))
p.parse()

# Error handling after parsing
if p.errors.error_status:
    p.errors.print()
    sys.exit(1)
else:
    # Print the AST, ST, or CS based on the flags
    if AST:
        p.printAST()
    else:
        if ST:
            p.printST()
        else:
            p.standardize()
            c = ControlStructureBuilder(p.ST)
            if CS:
                c.printCS()
            else:
                c.linerize()
                a = CSEMachine(c.control_structures,p.errors)
                a.apply_rules()
                if a.errors.error_status:
                    p.errors.print()
                    sys.exit(1)
                else:
                    a.print()



