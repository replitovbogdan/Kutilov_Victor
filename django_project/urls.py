# ============================================================
# ФАЙЛ: django_project/urls.py
# НАЗНАЧЕНИЕ: Корневой маршрутизатор URL всего проекта.
#   Связывает адреса (URL) с конкретными обработчиками (views).
#   Все запросы от браузера сначала попадают сюда.
# ============================================================

# ---------------------------------------------------------------
# БЛОК ИМПОРТОВ
# ---------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tasks import auth_views as custom_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('login/', custom_auth.login_view, name='login'),
    path('logout/', custom_auth.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ^ Добавляет маршруты для раздачи медиафайлов (работает только при DEBUG=True)
