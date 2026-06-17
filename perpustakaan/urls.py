
from django.urls import path
from . import views

urlpatterns = [
    # 1. Halaman Utama / Dashboard (http://127.0.0.1:8000/)
    path('', views.dashboard, name='dashboard'),
    path('buku/', views.list_buku, name='list_buku'),
    path('buku/detail/<int:id>/', views.detail_buku, name='detail_buku'),
    path('buku/tambah/', views.add_buku, name='add_buku'),    
    path('buku/edit/<int:id>/', views.edit_buku, name='edit_buku'),  
    path('buku/hapus/<int:id>/', views.hapus_buku, name='delete_buku'), 
    path('peminjaman/', views.list_peminjaman, name='list_peminjaman'),
    path('peminjaman/tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/kembali/<int:id>/', views.kembalikan_buku, name='kembalikan_buku'),
    path('siswa/', views.list_siswa, name='list_siswa'),
    path('siswa/detail/<int:id>/', views.detail_siswa, name='detail_siswa'),
    path('siswa/edit/<int:id>/', views.edit_siswa, name='edit_siswa'),
    path('siswa/hapus/<int:id>/', views.hapus_siswa, name='hapus_siswa'),
    path('siswa/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('siswa/', views.list_siswa, name='user_list'),
    path('user/edit/<int:id>/', views.edit_siswa, name='user_edit'),
    path('init/', views.init_db, name='init_db'),
]