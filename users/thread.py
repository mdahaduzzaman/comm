import threading
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

def send_email_thread(subject, message, sender_email, recepient_list):
    send_mail(subject, message, sender_email, recepient_list)

def generate_activation_email(user):
    """account activation email url"""
    # Generate a token for account activation
    token_generator = default_token_generator
    token = token_generator.make_token(user)

    # Construct activation link
    activation_url = reverse('activate_account', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})

    # Construct email content
    subject = 'Activate Your Account'
    message = render_to_string('email/activation_email.html', {'user': user, 'activation_url': activation_url})
    sender_email = settings.EMAIL_HOST_USER
    # send_email_thread(subject, message, sender_email, [user.email])

     # Start a new thread to send the email
    thread = threading.Thread(target=send_email_thread, args=(subject, message, sender_email, [user.email]))

    thread.start()


