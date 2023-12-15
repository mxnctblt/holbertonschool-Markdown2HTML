#!/usr/bin/python3
""" 
Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""

import hashlib
import re
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)

    with open(sys.argv[1], 'r') as r:
        with open(sys.argv[2], 'w') as w:
            ul_status = False
            for line in r:
                length = len(line)
                h = line.lstrip('#')
                hlevel = line.count('#')
                ul = line.lstrip('-')
                ul_element = length - len(ul)

                if 1 <= hlevel <= 7:
                    line = f"<h{hlevel}>{h.strip()}</h{hlevel}>\n"

                if ul_element:
                    if not ul_status:
                        w.write('<ul>\n')
                        ul_status = True
                    line = f"<li>{ul.strip()}</li>\n"
                if not ul_element and ul_status:
                    w.write('</ul>\n')
                    ul_status = False

                w.write(line)

    exit(0)