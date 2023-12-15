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
        exit(1)

    with open(sys.argv[1], 'r') as r:
        with open(sys.argv[2], 'w') as w:
            ol_status = False
            ul_status = False
            for line in r:
                length = len(line)
                # strip to get tag
                h = line.lstrip('#')
                hlevel = line.count('#')
                ol = line.lstrip('*')
                ol_element = length - len(ol)
                ul = line.lstrip('-')
                ul_element = length - len(ul)

                # headers
                if 1 <= hlevel <= 7:
                    line = f"<h{hlevel}>{h.strip()}</h{hlevel}>\n"

                # ordered list
                if ol_element:
                    if not ol_status:
                        w.write('<ol>\n')
                        ol_status = True
                    line = f"<li>{ol.strip()}</li>\n"
                if not ol_element and ol_status:
                    w.write('</ol>\n')
                    ol_status = False

                # unordered list
                if ul_element:
                    if not ul_status:
                        w.write('<ul>\n')
                        ul_status = True
                    line = f"<li>{ul.strip()}</li>\n"
                if not ul_element and ul_status:
                    w.write('</ul>\n')
                    ul_status = False

                w.write(line)

            # close tags if open and EOF
            if ol_status:
                w.write('</ol>\n')
            if ul_status:
                w.write('</ul>\n')

    exit(0)