#exception_email.py

"""
Exception Email Notification Module

This module provides a function to send email notifications in case of exceptions.

The send_exception_email function establishes a connection to an SMTP server and sends an email
with an exception message to a predefined list of recipients.

Usage:
1. Import the module: from exception_email import send_exception_email
2. Call the send_exception_email function with the exception message as a parameter.

Author: Chaudhary Muskaan
Date: 11 Oct 2023
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_exception_email(exception_message):
    # Initialize connection to email server
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    # Your sender name and email
    sender_name = "No Reply"
    sender_email = "no_reply@gmail.com"

    # Login with your email and password
    smtp.login('muskaantestmail@gmail.com', 'lxuq sjiv ryau nnsf')

    # Message function
    def message(subject="Error Notification", text=""):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = formataddr((sender_name, sender_email))
        msg.attach(MIMEText(text))
        return msg

    # Automating the process
    def auto():
        msg = message("Error Notification", "The program has been halted due to: " + exception_message)
        to = ["chaudharymuskan19@gmail.com", "chaudharymuskaan19@gmail.com", "lim9gu@gmail.com"]
        from_addr = formataddr((sender_name, sender_email))
        smtp.sendmail(from_addr=from_addr, to_addrs=to, msg=msg.as_string())

    # Send the exception email
    auto()

    # Close the connection
    smtp.quit()
