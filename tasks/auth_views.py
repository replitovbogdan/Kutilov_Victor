from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            error = True
    return render(request, 'registration/login.html', {'error': error})


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/login/')
