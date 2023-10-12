#import the module
from exception_email import send_exception_email

#code which can raise an exception
try:
    result = 10 / 0
except Exception as e:
    # Send an exception email with the exception message
    send_exception_email("An error has occcured in the system")