#shamelessly taken from threebarber's alertme project on gh
# requires requests, oauth2 and python-twitter packages
# -*- coding: utf-8 -*-
import time
import requests
import smtplib
from timeit import default_timer as timer
import oauth2 as oauth

#loading keys from another file
#safe to comment out the next 3 lines if you want to declare the key variable strings in this file
import sys
sys.path.append('/Users/Demian/Documents/projects/')
from twitterkeys import *

import twitter


api = twitter.Api(consumer_key=my_consumer_key,
                  consumer_secret=my_consumer_secret,
                  access_token_key=my_access_token_key,
                  access_token_secret=my_access_token_secret)



start = timer()

# notification functions

def post_tweet(subject, body):
    status = api.PostUpdate(subject + ' ' + body)
    print(status.text)


def send_email(user, pwd, recipient, subject, body): #snippet courtesy of david / email sending function

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd) #login to gmail server
        server.sendmail(FROM, TO, message) #actually perform sending of mail
        server.close() #end server
        print 'successfully sent the mail' #alert user mail was sent
    except Exception, e: #else tell user it failed and why (exception e)
        print "failed to send mail, " +str(e)

def main(): #main function

    with requests.Session() as c:
        url        =      'http://alexotoro.wordpress.com'
        wait_time  =      45 #customizable time to wait to check for changes IE every 5 secs

        page1 = c.get(url) #base page that will be compared against

        time.sleep(wait_time) #wait inbeetween initial retrieval and comparison actions

        page2 = c.get(url) #page to be compared against page1 / the base page

        if page1.content == page2.content: #if else statement to check if content of page remained same
            end = timer()
            if ((end-start)) >= 60:
                timeMinutes = (end-start) / 60
                print "[-]No Change Detected @ " +str(url)+ "\n[-]Elapsed Time: " +str(timeMinutes)+ " minutes"
            else:
                print '[-]No Change Detected @ ' +str(url)+ "\n[+]Elapsed Time: " +str((end-start))+ " seconds"


        else:
            end = timer()
            if int((end-start)) >= 60:
                timeMinutes = (end-start) / 60
                print '[+]Change Detected - \n[+]Elapsed Time: ' +str(timeMinutes)+ " minutes"  #if anything was changed - it sends an email alerting the user
            else:
                print '[+]Change Detected - \n[+]Elapsed Time: ' +str((end-start))+ " seconds"  #if anything was changed - it sends an email alerting the user

            #pick the notification type here
            #send_email(user, pwd, recipient, subject, body) #send notification email
            post_tweet(subject, body)

        page2  = None #clear page2 variable before looping through main function again

        #time.sleep(wait_time) optional wait beetween starting again

        main() #super simple easy loop method


if __name__ == "__main__": #start main function
    
    main()

