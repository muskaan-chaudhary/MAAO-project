'''
Automated Log File Emailer

This program monitors a directory and its subdirectories for newly added log files
and sends them via email. It uses the Watchdog library to detect file creation events
and Gmail to send emails with log file attachments.

The program is designed to be flexible and can be used to monitor any directory
structure for log files with the 'log' in the title and send them via email.

Usage:
1. Modify the email server, sender, and authentication settings.
2. Specify the directory to monitor in the code.
3. Run the program, and it will continuously monitor for log files and send them via email.

Author: Chaudhary Muskaan
Date: 11 Oct 2023
'''

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from datetime import date
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email.utils import formataddr

# Initialize connection to email server
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

sender_name = "No Reply"
sender_email = "no_reply@gmail.com"
# Login with your email and password
smtp.login('your_email@gmail.com', 'your_password')

# Initializing datetime module
today = str(date.today())



# Message function
def message(subject="Python Notification"+'', 
			text="", attachments=None):
	
	# Build message contents
	msg = MIMEMultipart()
	
	# Add Subject
	msg['Subject'] = subject
	# Format email address
	msg['From'] = formataddr((sender_name, sender_email))
	# Add text contents
	msg.attach(MIMEText(text))

	# Adding attachments from the directory
	if attachments is not None:
		
		# Check whether we have the list of attachments or not
		if type(attachments) is not list:
			attachments = [attachments]

		for one_attachment in attachments:

			with open(one_attachment, 'rb') as f:
				file = MIMEApplication(
					f.read(),
					name=os.path.basename(one_attachment)
				)
			file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(one_attachment))
			# Add the attachment to our message object
			msg.attach(file)
	return msg

# Automating the process
def auto(file_paths):
	msg = message("MAAO 0.7-m Robotic Observation Log " + today , " [TEST] \n This Email is sent automatically. \n Please find the attachments below. ", file_paths)
	to = ["email1@gmail.com", "email2@gmail.com", "email3.com"
	   ]
	
    
	from_addr = formataddr((sender_name, sender_email))
	# Send the email
	smtp.sendmail(from_addr=from_addr,
				to_addrs=to, msg=msg.as_string())

# Define the event handler for file changes
'''class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            #check for the log files
            if "log" in file_path.lower():
	            auto(file_path)'''

# Define the event handler for file changes
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.pending_files = []

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            # check for the log files
            if "log" in file_path.lower():
                self.pending_files.append(file_path)

    def send_pending_files(self):
        if self.pending_files:
            auto(self.pending_files)
            self.pending_files = []
					
				
if __name__ == "__main__":
    # Specify the directory to monitor
	try:
		while True:
			directory_to_watch = "/file/path/here"

			# Create an observer and link it to the event handler
			observer = Observer()
			event_handler = MyHandler()
			observer.schedule(event_handler, path=directory_to_watch, recursive=True)

			# Start the observer
			observer.start()

			try:
				while True:
					time.sleep(5) 
					event_handler.send_pending_files() # Adjust the interval as needed
			except KeyboardInterrupt:
				observer.stop()
	finally:
		observer.join()

# Close the connection
smtp.quit()
