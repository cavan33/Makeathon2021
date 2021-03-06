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


#Define the mechanism to show posts, sorted by time:
def show_jsonPosts(following):
    #Note: 'usernames' is the list of all usernames whose posts you want to see (followed users)
    #Returns: posts: a list of all the posts to be shown in the feed, in JSON format
    posts = []

    for u in following: #Each line of the usernames text file; or just a usernames array, as we will define it for now.
        dirname = '/var/www/hack2020/'+u+'/posts/'
        if not os.path.exists(dirname):
            continue
        for j in range(1, 1 + len(os.listdir(dirname))):
            with open(dirname+'post'+str(j)+'.json', 'r') as f:
                data = f.read()
                posts.append(data)
    return posts

#Collect the posts:
#Define the 'following' list:
f = open('/var/www/hack2020/'+username+'/'+'following.txt', 'r') 
followed_users = f.readlines() 
f.close()
following = [followed_users[i].strip() for i in range(len(followed_users))]
feed_posts = show_jsonPosts(following)
print("{",end="")
for i, p in enumerate(feed_posts):
    print('\"post' + str(i) + '":' + str(p), end="")
    if not i == len(feed_posts)-1:
        print(',',end="")
print("}", end="")
