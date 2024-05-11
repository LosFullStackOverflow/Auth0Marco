from django.shortcuts import render
import json
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, 'index.html')


def logout(request):
    auth_logout(request)
    return render(request, 'index.html')


def profile(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'index.html')
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }
    print(userdata['name'])
    context = {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'email': user.first_name
    }
    return render(request, 'profile.html', context)


def change_password(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            return render(request, 'index.html')
        print("AAAAA")
        user = request.user
        email = user.first_name
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if new password matches confirm password
        if new_password == confirm_password:
            # Assuming you have a function or endpoint in your API to change password
            api_url = f'http://127.0.0.1:8001/cliente/update/{email}/'
            print(api_url)
            payload = {
                'email': email,
                'password': current_password,
                'newPassword': new_password
            }
            # Make a POST request to your API
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(
                    request, "Failed to change password. Please try again.")

            return redirect('profile')
        else:
            messages.error(
                request, "New password and confirm password do not match.")
            return redirect('profile')
