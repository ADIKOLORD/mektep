from django.contrib import admin
from django.urls import path, include
from config.config import ADMIN_URL

BASE_URL = 'api/v1/'
urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path(BASE_URL + 'account/', include('account.urls')),
]
