from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .utils.processor import process_files, create_test_files, generate_charts
import base64
import os
import shutil


@csrf_exempt
def index(request):
    # If user not authenticated, handle login form
    if not request.user.is_authenticated:
        error = False
        if request.method == 'POST' and 'username' in request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Fall through to show main page below
            else:
                error = True
                return render(request, 'registration/login.html', {'error': error})
        else:
            return render(request, 'registration/login.html', {'error': False})

    # ---- User is authenticated: show main microservice page ----
    results = None
    charts = {}

    test_files = ['data.json', 'report.json', 'config.json', 'data.csv', 'backup.csv']
    test_files_exist = all(os.path.exists(f) for f in test_files)
    if not test_files_exist:
        create_test_files()

    if request.method == 'POST' and request.FILES.getlist('files'):
        uploaded_files = request.FILES.getlist('files')
        file_paths = []
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_dir, uploaded_file.name)
            if os.path.exists(file_path):
                name, ext = os.path.splitext(uploaded_file.name)
                counter = 1
                while os.path.exists(file_path):
                    file_path = os.path.join(upload_dir, f"{name}_{counter}{ext}")
                    counter += 1
            with open(file_path, 'wb') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)
            file_paths.append(file_path)

        if file_paths:
            results = process_files(file_paths)
            generate_charts(results)
            for chart_file in ['char7.png', 'char8.png', 'char9.png', 'char10.png']:
                if os.path.exists(chart_file):
                    with open(chart_file, 'rb') as img:
                        charts[chart_file.replace('.png', '')] = base64.b64encode(img.read()).decode()
    else:
        test_file_paths = [os.path.abspath(f) for f in test_files if os.path.exists(f)]
        if test_file_paths:
            results = process_files(test_file_paths)
            generate_charts(results)
            for chart_file in ['char7.png', 'char8.png', 'char9.png', 'char10.png']:
                if os.path.exists(chart_file):
                    with open(chart_file, 'rb') as img:
                        charts[chart_file.replace('.png', '')] = base64.b64encode(img.read()).decode()

    return render(request, 'tasks/index.html', {
        'results': results,
        'charts': charts,
        'full_name': 'Кутилов Б.А.',
    })


@csrf_exempt
def clean_uploads(request):
    if request.method == 'POST':
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)
            os.makedirs(upload_dir, exist_ok=True)
        for chart_file in ['char7.png', 'char8.png', 'char9.png', 'char10.png']:
            if os.path.exists(chart_file):
                os.remove(chart_file)
    return index(request)
