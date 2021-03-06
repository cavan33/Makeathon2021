#!/usr/bin/python3 -u
import sys
import os
import json

print('Content-Type: text/html\n\n')

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


f = open('/var/www/hack2020/'+username.strip()+'/'+'following.txt', 'r')
followed_users = f.readlines() 
f.close()
following = [followed_users[i].strip() for i in range(len(followed_users))]
all_users = {}

for i, un in enumerate(os.listdir('/var/www/hack2020/')):
    all_users[i] = {}
    all_users[i]['username'] = un
    if un in following:
        all_users[i]['is_friend'] = 1
    else:
        all_users[i]['is_friend'] = 0
print(json.dumps(all_users))
#print("{",end="")
#for i, p in enumerate(feed_posts):
#    print('\"post' + str(i) + '":' + str(p), end="")
#    if not i == len(feed_posts)-1:
#        print(',',end="")
#print("}", end="")
