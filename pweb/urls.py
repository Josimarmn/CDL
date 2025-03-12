from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #rota para view index
    path('home/', include ('home.urls')),
    path('admin/', admin.site.urls),
]
