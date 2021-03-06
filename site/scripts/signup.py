#!/usr/bin/python3 -u
import cgi
import cgitb
import sys
import json
import os

cgitb.enable()

form = cgi.FieldStorage()
if "username" not in form or "password" not in form:
    print('Set-Cookie: username=; Path=/');
    print('Set-Cookie: password=; Path=/');
    print("Content-Type: text/html\n\n")
    sys.exit(0)


#A check: print("Hello " + form['username'].value)
username = form['username'].value
password = form['password'].value
#Make variables to make a starting loan of 1000:
amt_money = 1000 #Default starting money value - substitute for linking your bank account
totalOwed = 0
numPayments = 0
repayLength = 0
intervalPay = 0
interestPercent = 0
loan_stats = {'amt_money': amt_money, 'interestRate': interestPercent / 100, 'totalOwed': 0, 'intervalPay': 0, 'repayLength': 0}

#Define the mechanism to save loans' data to the correct files:
def save_data(obj, filename):
    f = open(filename,'w')
    f.write(obj)
    f.close()

empty_field = None
#If the username folder is not created yet, create it, and create some txt files. Also, make the posts directory:
#Dirname for the one receiving the loan:
dirname = '/var/www/hack2020/'+username+'/'
if not os.path.exists(dirname):
    os.mkdir(dirname)
    os.mkdir(dirname+'/posts/')
    save_data(password, dirname+'password.txt')
    save_data("", dirname+'amt_money.txt')
    save_data("", dirname+'allLoans.txt')
    save_data("", dirname+'following.txt')
    save_data(json.dumps(loan_stats)+'\n', dirname+'loans_Received.txt')
else:
    print("Content-Type: text/html\n\n")
    print('You are already signed up. Contact an administrator if you forgot your password. Otherwise, we will log you in now.')
    quit()

#Now, log them in straight away:
#A check: print("Hello " + form['username'].value +" "+ form['lastname'].value)

#Check the username and password against a user folder:
passwordfilename = dirname+'password.txt'
with open(passwordfilename, 'r') as file:
    password_from_file = file.read()

if password_from_file.strip() == password.strip():
    #print("Login successful, " + username_in)
    print('Set-Cookie: logged_in=1; Path=/');
    print('Set-Cookie: username=' + username+ "; Path=/");
    print('Set-Cookie: password=' + password.strip() + "; Path=/");
else:
    #print("Login unsuccessful, " + username_in)
    print('Set-Cookie: logged_in=0; Path=/');
    print('Set-Cookie: username=' + username + "; Path=/");
    print('Set-Cookie: password=' + password.strip() + "; Path=/");


print("Content-Type: text/html\n\n")
