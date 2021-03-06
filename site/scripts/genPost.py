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
#import matplotlib.pyplot as plt

#NOTE that "post" now basically refers to an "instance" of the form sending data in, plus the graph that is made from that data (with times).

cgitb.enable()

form = cgi.FieldStorage()
#The line below says to quit if we don't receive the bare minimum:
if "temp1" not in form:
    print("Content-Type: text/html\n\n")
    sys.exit(0)

print("Content-Type: text/html\n\n")

def check_for_field(form, field):
    if (field in form.keys()):
        return form[field].value
    else:
        return "Not specified"


name_in = check_for_field(form,'name')
temperature_in = check_for_field(form,'temperature')
bac_in = check_for_field(form,'bac')
humidity_in = check_for_field(form,'humidity')
acc_in = check_for_field(form,'acc')
force_in = check_for_field(form,'force')


#Define the mechanism to save a post's data (but not its graphs/images) to a text file:
def save_postdata(post, filename):
    data = {}
    data['name'] = post.name
    data['temperature'] = post.temperature
    data['bac'] = post.bac
    data['humidity'] = post.humidity
    data['acc'] = post.acc
    data['force'] = post.force
    print(data)
    with open(filename, 'w') as outfile:  # Overwrites any existing file.
        json.dump(data, outfile, sort_keys = True)

#Class to generate a post, with a bunch of graphs/images plus some of the data that went in to making the graphs:
class genPost:
    name = ""
    temperature = 0
    bac = 0
    humidity = 0
    acc = 0
    force = 0
    date = ""
    epoch_sec = 0
    
    def __init__(self, name, temperature, bac, humidity, accx, accy, accz, force):
        self.name = name
        self.temperature = temperature
        self.bac = bac
        self.humidity = humidity
        self.acc = acc
        self.force = force
        #Get the time (since epoch) that we ran this script/instantiated this class, and then turn this into a "date posted" string:
        epoch_sec = time.time()
        epoch_sec_est = epoch_sec - 18000 #Remove 5 hours from the post times, to convert to EST (would be 14400 if it turns out to only need 4 hours)
        date = str(datetime.datetime.fromtimestamp(epoch_sec))
        postID = len(os.listdir('/var/www/make2021/posts/')) + 1
        self.date = date
        self.postID = postID # Simply goes up by 1 every time we save a new post
    
        """
        #Now, make the graphs:
        #Temperature graph:
        measurements = range(len(os.listdir('/var/www/make2021/posts/')) + 1) # x axis, + 1 because of our most recent, nonsaved observation
        fname = []
        temperatures = []
        for i in range(len(os.listdir('/var/www/make2021/posts/')) + 1): 
            fname[i-1] = '/var/www/make2021/posts/post'+i+'.json'
            temperatures[i-1] = fname[i-1]['temperature']
        temperatures.append(temperature) # This is the final observation we just got, but haven't yet saved using savepostdata


        # Initialize a figure (with one subplot)
        fig, ax = plt.subplots()

        #Plot measurement # vs temperature:
        ax.plot(measurements, temperatures, 'ok-', label='Temperature (F)', markersize = 4)

        #Title, Labels, and Legend
        ax.set_title('Temperature Readings (F)')
        ax.set_xlabel('Observation Number')
        ax.set_ylabel('Temperature')
        plt.legend(loc='upper right')
        tempgraphfname = '/var/www/make2021/posts/post'+str(post.postID)+'temperaturegraph.pdf'
        plt.savefig(tempgraphfname)
        """

   

#If the posts folder is not created yet, create it:
if not os.path.exists('/var/www/make2021/posts/'):
    os.mkdir('/var/www/make2021/posts/')

#Generate a post:
post = genPost(name_in, temperature_in, bac_in, humidity_in, accx_in, accy_in, accz_in, force_in)

#Save the post data (a text file, separate from the graphs):
save_postdata(post, '/var/www/make2021/posts/post'+str(post.postID)+'.json')


 def makeGraph(field):
    """
    Plots all values (x-axis = measurement number) of a certain inputted field (on the y-axis), and saves the figure as a PDF.
    """
    measurements = range(len(os.listdir('/var/www/make2021/posts/')) + 1) # x axis, + 1 because of our most recent, nonsaved observation
    fnames = []
    y = []
    for i in range(len(os.listdir('/var/www/make2021/posts/')) + 1): 
        fnames[i-1] = '/var/www/make2021/posts/post'+i+'.json'
        y[i-1] = fnames[i-1][field]

    # Initialize a figure (with one subplot)
    fig, ax = plt.subplots()

    #Plot:
    if field == 'temperature':
        ax.plot(measurements, y, 'ok-', label=post.name, markersize = 4)
        ax.set_title('Temperature Readings')
        ax.set_ylabel('Temperature (F)')
    elif field == 'bac':
        ax.plot(measurements, y, 'ob-', label=post.name, markersize = 4)
        ax.set_title('Blood-Alcohol Content Readings')
        ax.set_ylabel('BAC')
    elif field == 'humidity':
        ax.plot(measurements, y, 'ro-', label=post.name, markersize = 4)
        ax.set_title('Humidity Readings')
        ax.set_ylabel('Humidity (%)')
    elif field == 'acc':
        ax.plot(measurements, y, 'om-', label=post.name, markersize = 4)
        ax.set_title('Acceleration Scores')
        ax.set_ylabel('Acceleration (Score, 0-100)') # This likely needs to be edited later
    elif field == 'force':
        ax.plot(measurements, y, 'og-', label=post.name, markersize = 4)
        ax.set_title('Force Readings')
        ax.set_ylabel('Force (N)')

    ax.set_xlabel('Observation Number')
    plt.legend() # Maybe (loc='upper right')?
    graphfname = '/var/www/make2021/posts/post'+str(post.postID)+field+'graph.pdf'
    plt.savefig(graphfname)


makeGraph('temperature')
#Later:
"""
makeGraph('bac')
makeGraph('humidity')
makeGraph('acc')
makeGraph('force')
"""


##Originally from a different file: get all the data from all-time in order to make the graph of all times.
#loans = []
#file1 = open('/var/www/hack2020/'+username+'/'+'loans_Received.txt', 'r')
#lines = file1.readlines()
#for line in lines:
#    loans.append(json.loads(line))
#amt_money = sum([float(d['amt_money']) for d in loans])
#monthly_amt_owed = sum([float(d['intervalPay']) for d in loans])
#total_amt_owed = sum([float(d['totalOwed']) for d in loans])
#print(amt_money)
#print(monthly_amt_owed)
#print(total_amt_owed)

