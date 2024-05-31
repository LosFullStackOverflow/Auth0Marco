from django.shortcuts import render
import json
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.
apiUrlMachine = "127.0.0.1:8001"


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
    api_url = f'http://{apiUrlMachine}/cliente/'
    newCliente = {
        'email': userdata['name'],
        'nombre': userdata['name'].split('@')[0],
        'apellido': 'apellido',
        'pais': 'pais',
        'ciudad': 'ciudad',
        'celular': 3214330135,
        'password': '1234',
        'actividadEconomica': 'actividadEconomica',
        'empresa': 'empresa',
        'ingresos': 12000000,
        'pasivos': 1000000,
    }
    response = requests.post(api_url, json=newCliente)
    print(response)

    context = {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'email': user.first_name
    }
    return render(request, 'profile.html', context)


def metaData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        estado_actual = None
        if action == 'button1':
            # Handle action for Button 1
            estado_actual = 'Cancelada'
            messages.success(request, 'Estado actualizado a: Cancelada.')
        elif action == 'button2':
            # Handle action for Button 2
            estado_actual = 'En espera de oferta'
            messages.success(
                request, 'Estado actualizado a: En espera de oferta.')
        elif action == 'button3':
            # Handle action for Button 3
            estado_actual = 'Oferta creada'
            messages.success(
                request, 'Estado actualizado a: Oferta creada.')
        elif action == 'button4':
            # Handle action for Button 4
            estado_actual = 'Oferta aceptada'
            messages.success(
                request, 'Estado actualizado a: Oferta aceptada.')
        elif action == 'button5':
            # Handle action for Button 4
            estado_actual = 'Finalizado'
            messages.success(
                request, 'Estado actualizado a: Finalizado.')
        if estado_actual:
            user = request.user
            email = user.first_name

            api_url = f'http://{apiUrlMachine}/estado/{email}/'
            payload = {
                "estado": estado_actual
            }
            # Make a POST request to your API
            response = requests.post(api_url, json=payload)

        # Replace 'your_template_name' with the name of your template
        return redirect('metaData')
    return render(request, 'metaData.html')


def change_password(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            return render(request, 'index.html')
        user = request.user
        email = user.first_name
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if new password matches confirm password
        if new_password == confirm_password:
            # Assuming you have a function or endpoint in your API to change password
            apiUrlMachine = "127.0.0.1:8001"
            # apiUrlMachine = "34.68.167.238:8080"

            api_url = f'http://{apiUrlMachine}/cliente/update/{email}/'
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
