from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils.processor import process_files, create_test_files, generate_charts
import base64
import os
import shutil


@csrf_exempt
def index(request):
    # --- Login handling (no redirect, no cookies needed) ---
    if not request.user.is_authenticated:
        if request.method == 'POST' and 'username' in request.POST:
            user = authenticate(
                request,
                username=request.POST.get('username', ''),
                password=request.POST.get('password', ''),
            )
            if user is not None:
                auth_login(request, user)
                # fall through to render the main page immediately
            else:
                return render(request, 'registration/login.html', {'error': True})
        else:
            return render(request, 'registration/login.html', {'error': False})

    # --- Main microservice page (user is authenticated) ---
    results = None
    charts = {}

    test_files = ['data.json', 'report.json', 'config.json', 'data.csv', 'backup.csv']
    if not all(os.path.exists(f) for f in test_files):
        create_test_files()

    chart_files = ['char7.png', 'char8.png', 'char9.png', 'char10.png']

    if request.method == 'POST' and request.FILES.getlist('files'):
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_paths = []
        for uploaded_file in request.FILES.getlist('files'):
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
        results = process_files(file_paths)
        generate_charts(results)
    else:
        test_paths = [os.path.abspath(f) for f in test_files if os.path.exists(f)]
        if test_paths:
            results = process_files(test_paths)
            generate_charts(results)

    for cf in chart_files:
        if os.path.exists(cf):
            with open(cf, 'rb') as img:
                charts[cf.replace('.png', '')] = base64.b64encode(img.read()).decode()

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
        for cf in ['char7.png', 'char8.png', 'char9.png', 'char10.png']:
            if os.path.exists(cf):
                os.remove(cf)
    return index(request)
