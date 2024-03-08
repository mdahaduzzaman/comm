import threading
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def send_email_thread(subject, html_content, sender_email, recepient_list):
    email_message = EmailMessage(subject, html_content, sender_email, recepient_list)
    email_message.content_subtype = "html"  # Set the content type to HTML
                
    # Send the email
    try:
        email_message.send()
        print("mail send")
    except Exception as e:
        print(e)

def generate_activation_email(user, host_url):
    """account activation email url"""
    # Generate a token for account activation
    token_generator = default_token_generator
    token = token_generator.make_token(user)

    # Construct activation link
    activation_url = reverse('activate_account', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})

    activation_url = host_url+activation_url

    # Construct email content
    subject = 'Activate Your Account'
    html_content = render_to_string('email/activation_email.html', {'user': user, 'activation_url': activation_url})
    sender_email = settings.EMAIL_HOST_USER
    
    # Start a new thread to send the email
    thread = threading.Thread(target=send_email_thread, args=(subject, html_content, sender_email, [user.email]))

    thread.start()


def generate_password_reset_email(user, host_url):
    """generate password reset email url and send the email"""
    # Generate a token for reset password
    token_generator = default_token_generator
    token = token_generator.make_token(user)

    # Construct reset password link
    activation_url = reverse('reset_password', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})

    activation_url = host_url+activation_url

    # Construct email content
    subject = 'Activate Your Account'
    html_content = render_to_string('email/reset_password_email.html', {'user': user, 'activation_url': activation_url})
    sender_email = settings.EMAIL_HOST_USER
    
    # Start a new thread to send the email
    thread = threading.Thread(target=send_email_thread, args=(subject, html_content, sender_email, [user.email]))

    thread.start()


