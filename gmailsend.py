#!/usr/bin/env python2
"""Send file as message through gmail

Usage:
    ./gmailsend.py sender recipient subject body_file passwd
"""

# Importing modules
from email.mime.text import MIMEText
import smtplib
import getpass
import sys

# Parse user input
try:
    sender = sys.argv[1]
    recipient = sys.argv[2]
    subject = sys.argv[3]
    body_file = sys.argv[4]
    passwd = sys.argv[5]
except:
    print __doc__
    sys.exit(1)
 
# Sends an e-mail to the specified recipient.
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

with open(body_file, 'rb') as content:
    msg = MIMEText(content.read())

msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject

session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
session.ehlo()
session.starttls()
session.ehlo
session.login(sender, passwd) # getpass.getpass("Password: ") )
 
session.sendmail(sender, recipient, msg.as_string())
session.quit()

