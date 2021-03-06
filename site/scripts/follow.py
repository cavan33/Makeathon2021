#!/usr/bin/python3 -u
import cgi
import cgitb
import json
import sys
import os

cgitb.enable()
print("Content-Type: text/html\n\n")

form = cgi.FieldStorage()
if "username" not in form:
    print("username not in form")
    sys.exit(0)

following_value = form.getlist("username")
#print(value)
following = ",".join(following_value)
#print(following)


#Read the cookies that have been established:
handler = {} # A dictionary which will house the cookie names and cookie values
if 'HTTP_COOKIE' in os.environ:
    cookies = os.environ['HTTP_COOKIE']
    cookies = cookies.split('; ')
    for cookie in cookies:
        cookie = cookie.split('=')
        handler[cookie[0]] = cookie[1]
#handler now has all 3 cookies we want.
#Now, do checks with these cookies:
username = ""
if 'logged_in' in handler and handler['logged_in'] == '1': #(Checked if logged in)
    with open('/var/www/hack2020/'+handler['username']+'/'+'password.txt','r') as file:
        fp = file.read()

    if handler['password'].strip() == fp.strip():
        username = handler['username']
    else:
        print('Wrong password!')
        quit()
else:
    print('not logged in')
    quit()

#Define the mechanism to save the following list to a text file:
def save_following(obj, filename):
	f = open(filename,'w')
	for i in range(len(obj)):
		f.write(obj[i] + '\n')
	f.close()


save_following(following_value, '/var/www/hack2020/'+username+'/'+'following.txt')
