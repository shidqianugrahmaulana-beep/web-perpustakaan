<<<<<<< HEAD
from django.db import models

# Pastikan huruf S-nya besar!
class Siswa(models.Model): 
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Aktif')

    def __str__(self):
=======
from django.db import models

# Pastikan huruf S-nya besar!
class Siswa(models.Model): 
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Aktif')

    def __str__(self):
>>>>>>> c3b90f2132341348918c3e24a51488723f093317
        return self.nama