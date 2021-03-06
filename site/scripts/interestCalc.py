#!/usr/bin/python3 -u
import cgi
import cgitb
import json
import sys
import os

cgitb.enable()
print("Content-Type: text/html\n\n")

form = cgi.FieldStorage()
if ("amt_money" not in form or "interestPercent" not in form or "don_or_loan" not in form or "repayLength" not in form or "to" not in form):
    #print("field not in form: " + str(form))
    sys.exit(0)

#A check: print("Hello " + form['username'].value)
amt_money = form['amt_money'].value
interestPercent = form['interestPercent'].value
don_or_loan = form['don_or_loan'].value.lower()
repayLength = form['repayLength'].value
to = form['to'].value

#------------------------------------------------------------------------------
#Aside: Check all cookies
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
#------------------------------------------------------------------------------

#Convert the numerical values to floats:
amt_money = float(amt_money)
interestPercent = float(interestPercent)
repayLength = float(repayLength)

#Define the mechanism to save loans' data to the correct files:
def save_data(obj, objfilename, dirname):
    #Dir name will be the username folder, since all our stats are text files within that folder
    filename = dirname + objfilename
    f = open(filename,'a')
    f.write(json.dumps(obj)+'\n')
    f.close()
#Dirname for the loaner:
dirname = '/var/www/hack2020/'+username+'/'
#Dirname for the one receiving the loan:
dirname2 = '/var/www/hack2020/'+to+'/'

#Define the function to calculate the financial data from the inputs:
def calc_amounts(amt_money, interestPercent, don_or_loan, repayLength):
    # This program calculates repayments on an interest rate loan/mortgage, and stores the stats in a dictionary
    flag=0
    if(don_or_loan == 'donation'):
        totalOwed = 0
        numPayments = 0
        repayLength = 0
        intervalPay = 0
        interestPercent = 0
        loan_stats = {'amt_money': amt_money, 'interestRate': interestPercent / 100, 'totalOwed': 0, 'intervalPay': 0, 'repayLength': 0}
        flag = 1
    elif(don_or_loan != 'loan'):
        print("Must be a 'Donation' or a 'Loan', got: " + don_or_loan)
        flag = 1
        sys.exit(0)

    interestRate = interestPercent / 100
    if (flag != 1):
        interval = "month"
        #Could have options, but hard coded is easier.
        #working out the number of payments per year over the course of the loan period.
        if (interval == "week"):
            numPayments = 365.2422/7
        elif (interval == "month"):
            numPayments = 12
        elif (interval == "year"):
            numPayments = 1
        else:
            print("Invalid interval of payments. Try again.")
            sys.exit(0)

        #Formula
        #A = P((1+r/n)^(n*t))
        #   A = Total Repayment (totalOwed)
        #   P = Principal Loan Amount (principal)
        #   r = Annual Interest Rate, as a decimal (interestRate)
        #   n = Number of Payments per unit t [i.e. years] (numPayments)
        #   t = Length of the loan [in years] (repayLength)

        totalOwed = amt_money*((1+interestRate/numPayments)**(numPayments*repayLength))
        #Now divide this by the total number of payments over all the years of the load to find the payment in each interval:
        intervalPay = totalOwed/(numPayments*repayLength)
        loan_stats = {'amt_money': amt_money, 'interestRate': interestRate, 'totalOwed': totalOwed, 'intervalPay': intervalPay, 'repayLength': repayLength}
    return loan_stats

loan_stats = calc_amounts(amt_money, interestPercent, don_or_loan, repayLength)
#Now that we have all the stats and the interest for the loan, save the data to the correct files:
#For the loaner:
save_data(loan_stats, 'allLoans.txt', dirname)
#For the one receiving the loan:
save_data(loan_stats, 'loans_Received.txt', dirname2)

