from authentication.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello world")
    
def login_process(request):

    if request.method == 'POST':

        authentication_form = AuthenticationForm(request.POST)

        if authentication_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home:index'))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return render(request, 'authentication/login.html', {'authentication_form' : authentication_form, 'is_invalid_credentials' : True,})
        else:
            return render(request, 'authentication/login.html', {'authentication_form' : authentication_form,})
    else:
        return render(request, 'authentication/login.html', {'is_invalid_credentials' : False,})

@login_required
def logout_process(request):

    logout(request)
    return HttpResponseRedirect(reverse('home:index'))
