#!/usr/bin/python3 -u

import cgi
import cgitb
import sys

cgitb.enable()
print("Content-Type: text/html\n\n")

form = cgi.FieldStorage()
if "fname" not in form or "lname" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the name and addr fields.")
    sys.exit(0)
print("Hello " + form['fname'].value +" "+ form['lname'].value)

