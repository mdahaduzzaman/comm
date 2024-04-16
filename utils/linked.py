# views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from django.urls import reverse

LINKEDIN_CLIENT_ID = ''
LINKEDIN_CLIENT_SECRET = ''
REDIRECT_URI = "http://localhost:8000/linkedin/callback/"

def home(request):
    return render(request, "social/home.html")


def linkedin_login(request):
    # Define the scopes you want to request

    scopes = ['email', 'openid', 'profile']
    
    # Concatenate the scopes with '%20' separator
    scope_string = "%20".join(scopes)

    print("scope_string", scope_string)
    
    # Redirect users to LinkedIn's authorization page with the specified scopes
    return redirect(f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={LINKEDIN_CLIENT_ID}&scope={scope_string}&redirect_uri={REDIRECT_URI}")


def linkedin_callback(request):
    # Handle LinkedIn's authorization callback
    code = request.GET.get('code')
    print("code", code)
    if code:
        # Exchange the authorization code for an access token
        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken',
                                 params={'grant_type': 'authorization_code',
                                         'code': code,
                                         'redirect_uri': REDIRECT_URI,
                                         'client_id': LINKEDIN_CLIENT_ID,
                                         'client_secret': LINKEDIN_CLIENT_SECRET})
        print("response", response.json())
        if response.status_code == 200:
            access_token = response.json()['access_token']
            # Use the access token to make requests to LinkedIn API
            # Example: Fetch user profile
            profile_response = requests.get('https://api.linkedin.com/v2/userinfo',
                                            headers={'Authorization': f'Bearer {access_token}'})
            print("profile_response", profile_response.json())
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                print("profile_data", profile_data)
                # Process the profile data as needed
                return HttpResponse("Successfully authenticated with LinkedIn")
    return HttpResponse("Failed to authenticate with LinkedIn")
