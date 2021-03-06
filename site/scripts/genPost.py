#!/usr/bin/python3 -u
import cgi
import cgitb
import sys
import os
import time
import datetime
import json
#import pickle
#import numpy as np

cgitb.enable()

form = cgi.FieldStorage()
if "content" not in form or "interest" not in form:
    print("Content-Type: text/html\n\n")
    sys.exit(0)

print("Content-Type: text/html\n\n")


#A check: print("Hello " + form['username'].value)
content_in = form['content'].value
interestPercent_in = form['interest'].value
amt_money_in = form['amt_money'].value
#amt_money_in = 100


#Read the cookies that have been established:
handler = {}
if 'HTTP_COOKIE' in os.environ:
    cookies = os.environ['HTTP_COOKIE']
    cookies = cookies.split('; ')
    for cookie in cookies:
        cookie = cookie.split('=')
        handler[cookie[0]] = cookie[1]
#Hopefully, handler now has all 3 cookies we want.
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

#Define the mechanism to save posts' data to a file:
def save_postdata(post, filename):
    data = {}
    data['username'] = post.username
    data['content'] = post.content
    data['interestPercent'] = post.interestPercent
    data['amt_money'] = post.amt_money
    data['postID'] = post.postID
    data['loans'] = post.loans
    data['whoLoaned'] = post.whoLoaned
    data['date'] = post.date
    print(data)
    with open(filename, 'w') as outfile:  # Overwrites any existing file.
        json.dump(data, outfile, sort_keys = True)

#Class to generate a post and its data:
class genPost:
    username = ""
    content = ""
    interestPercent = 0
    postID = 0
    amt_money = 0
    loans = {}
    whoLoaned = []
    date = ""
    epoch_sec = 0
    
    def __init__(self, username, content, interestPercent, amt_money):
        self.username = username
        self.content = content
        self.interestPercent = interestPercent
        self.amt_money = amt_money
        #Get the time (since epoch) that we ran this script/instantiated this class, and then turn this into a "date posted" string:
        epoch_sec = time.time()
        epoch_sec_est = epoch_sec - 14400 #Remove 4 hours from the post times, to convert to EST
        date = str(datetime.datetime.fromtimestamp(epoch_sec))
        postID = len(os.listdir('/var/www/hack2020/'+username+'/posts/')) + 1
        self.date = date
        self.postID = postID

#If the posts folder is not created yet, create it:
if not os.path.exists('/var/www/hack2020/'+username+'/posts/'):
    os.mkdir('/var/www/hack2020/'+username+'/posts/')

#Generate a post:
post = genPost(username, content_in, interestPercent_in, amt_money_in)
#Checks:
#print(post.text)
#print(post.date)

#Save the post:
save_postdata(post, '/var/www/hack2020/'+post.username+'/posts/post'+str(post.postID)+'.json')
