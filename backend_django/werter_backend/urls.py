from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/core/', include('core.urls')),
]
