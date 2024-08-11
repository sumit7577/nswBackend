import re
from django.core.mail import EmailMessage
from django.conf import settings



def is_email(input_string):
    # Regular expression for validating email addresses
    email_regex = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9\.]+$'
    return re.match(email_regex, input_string) is not None

def is_phone(input_string):
    # Regular expression for validating phone numbers
    phone_regex = r'^\+?[\d\s-]{10}$'
    return re.match(phone_regex, input_string) is not None


# def send_mail(email, subject, message):
#     recipient_email = email 
#     sender_email = settings.EMAIL_HOST_USER 
#     email_send = EmailMessage(subject, message, sender_email,[recipient_email])
#     email_send.content_subtype = 'html'  # Set the content type to HTML
#     # Send the email
#     email_send.send()
def send_register_account_otp_mail(email, otp ):
    subject = 'Hello from HelloAPP!'
    message = f'This is a email sent from NSW for verify your mail using the OTP - {otp}.'
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [email]
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()