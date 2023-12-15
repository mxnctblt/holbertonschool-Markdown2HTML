#!/usr/bin/python3
""" 
Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        print(file=sys.stderr)
        exit(1)
    else :
        exit(0)