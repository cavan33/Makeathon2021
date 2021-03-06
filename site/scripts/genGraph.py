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

#NOTE that "post" now basically refers to an "instance" of the form sending data in, plus the graph that is made from that data (with times).

cgitb.enable()

form = cgi.FieldStorage()
#The line below says to quit if we don't receive the bare minimum:
if "name" not in form:
    print("Content-Type: text/html\n\n")
    sys.exit(0)

print("Content-Type: text/html\n\n")


#A check: print("Hello " + form['username'].value)
name_in = form['name'].value
temperature_in = form['temperature'].value
bac_in = form['bac'].value
humidity_in = form['humidity'].value
accx_in = form['accx'].value
accy_in = form['accy'].value
accz_in = form['accz'].value
force_in = form['force'].value


#Define the mechanism to save the sent-in data to a file:
def save_data(post, filename):
    data = {}
    data['name'] = post.name
    data['temperature'] = post.temperature
    data['bac'] = post.bac
    data['humidity'] = post.humidity
    data['accx'] = post.accx
    data['accy'] = post.accy
    data['accz'] = post.accz
    data['force'] = post.force
    data['graph'] = post.graph
    print(data)
    with open(filename, 'w') as outfile:  # Overwrites any existing file.
        json.dump(data, outfile, sort_keys = True)

#Class to generate a graph and its data:
class genGraph:
    name = ""
    temperature = 0
    bac = 0
    humidity = 0
    accx = 0
    accy = 0
    accz = 0
    force = 0
    date = ""
    epoch_sec = 0
    
    def __init__(self, name, temperature, bac, humidity, accx, accy, accz, force):
        self.name = name
        self.temperature = temperature
        self.bac = bac
        self.humidity = humidity
        self.accx = accx
        self.accy = accy
        self.accz = accz
        self.force = force
        #Get the time (since epoch) that we ran this script/instantiated this class, and then turn this into a "date posted" string:
        epoch_sec = time.time()
        epoch_sec_est = epoch_sec - 18000 #Remove 5 hours from the post times, to convert to EST (would be 14400 if it turns out to only need 4 hours)
        date = str(datetime.datetime.fromtimestamp(epoch_sec))
        graphID = len(os.listdir('/var/www/make2021/graphs/')) + 1
        self.date = date
        self.graphID = graphID # Simply goes up by 1 every time we save a new graph

    #Now, make the graphs:












#If the posts folder is not created yet, create it:
if not os.path.exists('/var/www/make2021/graphs/'):
    os.mkdir('/var/www/make2021/graphs/')

#Generate a graph:
post = genGraph(name_in, temperature_in, bac_in, humidity_in, accx_in, accy_in, accz_in, force_in)
#Checks:
#print()

#Save the post:
save_graph(post, '/var/www/make2021/graphs/post'+str(post.postID)+'.json')




#Originally from a different file: get all the data from all-time in order to make the graph of all times.
loans = []
file1 = open('/var/www/hack2020/'+username+'/'+'loans_Received.txt', 'r')
lines = file1.readlines()
for line in lines:
    loans.append(json.loads(line))
amt_money = sum([float(d['amt_money']) for d in loans])
monthly_amt_owed = sum([float(d['intervalPay']) for d in loans])
total_amt_owed = sum([float(d['totalOwed']) for d in loans])
print(amt_money)
print(monthly_amt_owed)
print(total_amt_owed)

