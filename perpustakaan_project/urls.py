<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('perpustakaan.urls')), # Mengarah ke file B menggunakan string
=======
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('perpustakaan.urls')), # Mengarah ke file B menggunakan string
>>>>>>> c3b90f2132341348918c3e24a51488723f093317
]