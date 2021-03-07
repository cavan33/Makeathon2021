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
import matplotlib.pyplot as plt

#NOTE that "post" now basically refers to an "instance" of the form sending data in, plus the graph that is made from that data (with times).

cgitb.enable()

form = cgi.FieldStorage()

print("Content-Type: text/html\n\n")

def check_for_field(form, field):
    if (field in form.keys()):
        return form[field].value
    else:
        return "Not specified"


name_in = check_for_field(form,'name')
temperature_in = check_for_field(form,'temperature')
gas_in = check_for_field(form,'gas')
humidity_in = check_for_field(form,'humidity')
acc_in = check_for_field(form,'acc')
force_in = check_for_field(form,'force')



#Define the mechanism to save a post's data (but not its graphs/images) to a text file:
def save_postdata(post, filename):
    data = {}
    data['name'] = post.name
    data['temperature'] = post.temperature
    data['gas'] = post.gas
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
    gas = 0
    humidity = 0
    acc = 0
    force = 0
    date = ""
    epoch_sec = 0
    
    def __init__(self, name, temperature, gas, humidity, acc, force):
        self.name = name
        self.temperature = temperature
        self.gas = gas
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


#Generate a post:
post = genPost(name_in, temperature_in, gas_in, humidity_in, acc_in, force_in)

#If the post's folder is not created yet, create it:
if not os.path.exists('/var/www/make2021/posts/post'+str(post.postID)+'/'):
    os.mkdir('/var/www/make2021/posts/post'+str(post.postID)+'/')

#Save the post data (a text file, separate from the graphs):
save_postdata(post, '/var/www/make2021/posts/post'+str(post.postID)+'/data.json')


def makeGraph(field):
    """
    Plots all values (x-axis = measurement number) of a certain inputted field (on the y-axis), and saves the figure as a PDF.
    """
    measurements = range(1, len(os.listdir('/var/www/make2021/posts/')) + 1) # x axis, + 1 because of our most recent, nonsaved observation
    fnames = [None]*len(os.listdir('/var/www/make2021/posts/'))
    y = []
    x = []
    cnt = 1
    for i in measurements: 
        fnames[i-1] = '/var/www/make2021/posts/post'+str(i)+'/data.json'
        with open(fnames[i-1]) as f:
              data = json.load(f)
        if(data[field] != "Not specified"):
            y.append(float(data[field]))
            x.append(cnt)
            cnt = cnt + 1

    # Initialize a figure (with one subplot)
    fig, ax = plt.subplots()
    label = post.name+"'s Data"

    #Plot:
    if field == 'temperature':
        ax.plot(x, y, 'ok-', label=label, markersize = 4);
        ax.set_title('Temperature Readings')
        ax.set_ylabel('Temperature (F)')
    elif field == 'gas':
        ax.plot(x, y, 'ob-', label=label, markersize = 4);
        ax.set_title('Gas (Alcohol) Readings')
        ax.set_ylabel('Gas Conc. (ppm)')
    elif field == 'humidity':
        ax.plot(x, y, 'ro-', label=label, markersize = 4);
        ax.set_title('Humidity Readings')
        ax.set_ylabel('Humidity (%)')
    elif field == 'acc':
        ax.plot(x, y, 'om-', label=label, markersize = 4);
        ax.set_title('Reaction Time (Average)')
        ax.set_ylabel('Time (ms)') # This likely needs to be edited later
    elif field == 'force':
        ax.plot(x, y, 'og-', label=label, markersize = 4);
        ax.set_title('Force/Weight Readings')
        ax.set_ylabel('Force (lbs)')

    ax.set_xlabel('Observation Number')
    if post.name != "Not specified":
        plt.legend() # Maybe (loc='upper right')?

    graphfname = '/var/www/html/Makeathon2021/site/html/'+field+'graph.pdf'
    # = '/var/www/make2021/posts/post'+str(post.postID)+'/'+field+'graph.pdf'
    plt.savefig(graphfname)


makeGraph('temperature')
makeGraph('gas')
makeGraph('acc')
makeGraph('force')

