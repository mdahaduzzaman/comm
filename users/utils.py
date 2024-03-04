from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from users.models import User

def activate_account(uidb64, token):
    """Activate the user by if activation done then send True otherwise send False"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = default_token_generator
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    else:
        return False