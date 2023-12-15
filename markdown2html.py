#!/usr/bin/python3
""" 
Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""

import hashlib
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
            p_status = False
            for line in r:

                # initialize counters for bold and emphasis
                bold_counter = 0
                emphasis_counter = 0

                # replace ** with <b> and </b>
                while '**' in line:
                    if bold_counter % 2 == 0:
                        line = line.replace('**', '<b>', 1)
                    else:
                        line = line.replace('**', '</b>', 1)
                    bold_counter += 1

                # replace __ with <em> and </em>
                while '__' in line:
                    if emphasis_counter % 2 == 0:
                        line = line.replace('__', '<em>', 1)
                    else:
                        line = line.replace('__', '</em>', 1)
                    emphasis_counter += 1
                
                # convert in MD5
                while '[[' in line and ']]' in line:
                    start = line.find('[[')
                    end = line.find(']]')
                    if start < end:
                        text = line[start + 2:end]
                        md5_text = hashlib.md5(text.encode()).hexdigest()
                        line = line[:start] + md5_text + line[end + 2:]

                # remove all c
                while '((' in line and '))' in line:
                    start = line.find('((')
                    end = line.find('))')
                    if start < end:
                        text = line[start + 2:end]
                        text_without_c = text.replace('c', '').replace('C', '')
                        line = line[:start] + text_without_c + line[end + 2:]

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
                
                # paragraphs and line breaks
                if not (hlevel or ol_status or ul_status):
                    if not p_status and length > 1:
                        w.write('<p>\n')
                        p_status = True
                    elif length > 1:
                        w.write('<br/>\n')
                    elif p_status:
                        w.write('</p>\n')
                        p_status = False
            
                if length > 1:
                    w.write(line)

            # close tags if open and EOF
            if ol_status:
                w.write('</ol>\n')
            if ul_status:
                w.write('</ul>\n')
            if p_status:
                w.write('</p>\n')

    # exit with a success status code
    exit(0)