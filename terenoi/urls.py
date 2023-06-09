"""terenoi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager/', include('manager.urls', namespace='manager')),
    path('admin/report/', include('report.urls', namespace='report')),
    path('api/auth/', include('authapp.urls', namespace='authapp')),
    path('api/user/', include('profileapp.urls', namespace='profile')),
    path('api/lessons/', include('lessons.urls', namespace='lessons')),
    path('api/courses/', include('courses.urls', namespace='courses')),
    path('api/finance/', include('finance.urls', namespace='finance')),
    path('api/settings/', include('settings.urls', namespace='settings')),
    path('api/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/library/', include('library.urls', namespace='library')),
    path('api/amocrm/', include('AmoCRM.urls', namespace='amo')),
    path('api/manager/', include('manager.urls', namespace='manager')),
    path('', RedirectView.as_view(url='admin/', permanent=False), name='index'),

]

urlpatterns += doc_urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
