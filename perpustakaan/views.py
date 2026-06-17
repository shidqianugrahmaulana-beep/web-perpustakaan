
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connection
# HAPUS BARIS: from .models import Siswa (jika masih ada)
# 1. Fungsi Dashboard Utama (Dinamis)
def dashboard(request):
    with connection.cursor() as cursor:
        # 1. Hitung akumulasi total unit buku (SUM dari kolom stok)
        cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM buku;")
        total_buku = cursor.fetchone()[0]

        # 2. Hitung total judul buku unik
        cursor.execute("SELECT COUNT(*) FROM buku;")
        total_judul = cursor.fetchone()[0]

        # 3. Hitung peminjaman aktif (Sedang Dipinjam)
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam';")
        sedang_dipinjam = cursor.fetchone()[0]

        # 4. Hitung peminjaman yang selesai (Sudah Dikembalikan)
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan';")
        sudah_dikembalikan = cursor.fetchone()[0]

        # 5. Ambil data judul dan stok untuk progress bar "Distribusi Stok Buku"
        cursor.execute("SELECT judul, stok FROM buku ORDER BY id ASC LIMIT 5;")
        buku_rows = cursor.fetchall()
        distribusi_buku = [{'judul': r[0], 'stok': r[1]} for r in buku_rows]

    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'distribusi_buku': distribusi_buku,
    }
    return render(request, 'app_perpus/index.html', context)
# 2. Fungsi Inisialisasi Tabel Database (Sudah Dibenerin Bug-nya)
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse  # Pastikan baris ini ada di paling atas file views.py

from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

def init_db(request):
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS buku;")
        cursor.execute("DROP TABLE IF EXISTS peminjaman;")
        cursor.execute("DROP TABLE IF EXISTS siswa;")
        
        # Tabel Buku
        cursor.execute("""
            CREATE TABLE buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                pengarang TEXT,
                kategori TEXT,
                penerbit TEXT,
                tahun INTEGER,
                rak TEXT,
                stok INTEGER
            );
        """)
        
        # Tabel Peminjaman (Pakai nama_siswa agar singkron dengan views kamu)
        cursor.execute("""
            CREATE TABLE peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_siswa TEXT NOT NULL,
                judul_buku TEXT NOT NULL,
                tanggal_pinjam TEXT NOT NULL,
                tanggal_kembali TEXT NOT NULL,
                keperluan TEXT,
                petugas TEXT,
                status TEXT NOT NULL
            );
        """)
        
        # Tabel Siswa/User
        cursor.execute("""
            CREATE TABLE siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT NOT NULL,
                nama TEXT NOT NULL,
                kelas TEXT NOT NULL,
                status TEXT NOT NULL
            );
        """)
        
        # Data Dummy Buku
        cursor.extend([
            cursor.execute("INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun, rak, stok) VALUES ('Laskar Pelangi', 'Andrea Hirata', 'Novel', 'Bentang Pustaka', 2005, 'Rak A-01', 5);"),
            cursor.execute("INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun, rak, stok) VALUES ('Bumi', 'Tere Liye', 'Novel', 'Gramedia Pustaka Utama', 2014, 'Rak A-02', 7);")
        ])
        
        # Data Dummy Peminjaman
        cursor.execute("""
            INSERT INTO peminjaman (nama_siswa, judul_buku, tanggal_pinjam, tanggal_kembali, keperluan, petugas, status) 
            VALUES ('Roni', 'Laskar Pelangi', '01 Jun 2026', '08 Jun 2026', 'Tugas sekolah Referensi tugas Bahasa Indonesia.', 'Budi Siregar', 'Dipinjam');
        """)
        
        # Data Dummy Siswa (Sesuai persis dengan gambar mockup kamu!)
        cursor.execute("INSERT INTO siswa (nis, nama, kelas, status) VALUES ('2026001', 'Roni', 'XI IPA 1', 'Aktif');")
        cursor.execute("INSERT INTO siswa (nis, nama, kelas, status) VALUES ('2026002', 'Sinta', 'XI IPS 2', 'Aktif');")
        cursor.execute("INSERT INTO siswa (nis, nama, kelas, status) VALUES ('2026003', 'Dewi Anggraini', 'X IPA 3', 'Aktif');")
        cursor.execute("INSERT INTO siswa (nis, nama, kelas, status) VALUES ('2026004', 'Bima Pratama', 'XII IPS 1', 'Aktif');")

    return HttpResponse("<h1 style='color: green; text-align: center; font-family: sans-serif; margin-top: 50px;'>✓ DATABASE REFRESHED: Data User/Siswa Siap Dipakai!</h1>")

def tambah_peminjaman(request):
    if request.method == 'POST':
        # Ambil nama_siswa dari form HTML kamu
        nama_siswa = request.POST.get('nama_siswa')
        judul_buku = request.POST.get('judul_buku')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        tanggal_kembali = request.POST.get('tanggal_kembali')
        keperluan = request.POST.get('keperluan')
        
        with connection.cursor() as cursor:
            # Gunakan f-string variabel di bawah ini untuk input form dinamis
            cursor.execute(f"""
                INSERT INTO peminjaman (nama_siswa, judul_buku, tanggal_pinjam, tanggal_kembali, keperluan, petugas, status)
                VALUES ('{nama_siswa}', '{judul_buku}', '{tanggal_pinjam}', '{tanggal_kembali}', '{keperluan}', 'Budi Siregar', 'Dipinjam');
            """)
        return redirect('list_peminjaman')
        
    return render(request, 'app_perpus/tambah_peminjaman.html')

# 3. Fungsi Menampilkan Daftar Siswa (User) dari Database
# 1. Tampilkan Daftar Siswa
# Halaman Utama Daftar User/Siswa
from django.shortcuts import render
from django.db import connection

def list_siswa(request):
    # Ambil seluruh baris data siswa yang tersimpan di DB
    semua_siswa = Siswa.objects.all()
    
    # Render ke folder app_perpus dan kirim variabelnya
    return render(request, 'app_perpus/list_siswa.html', {'daftar_user': semua_siswa})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Siswa # Sesuaikan dengan nama model siswa kamu

# 1. Pastikan fungsi list_siswa kamu sudah ada seperti ini
def list_siswa(request):
    semua_siswa = Siswa.objects.all()
    # ARTIKAN KE FOLDER app_perpus
    return render(request, 'app_perpus/list_siswa.html', {'daftar_user': semua_siswa})

# 2. TAMBAHKAN ATAU PASTIKAN FUNGSI INI ADA DI BAWAHNYA:
from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa

def edit_siswa(request, id):
    # 1. Ambil data siswa yang akan diedit berdasarkan ID urut di URL
    siswa_data = get_object_or_404(Siswa, id=id)
    
    # 2. Jika admin menekan tombol "Perbarui User" (Kirim POST data)
    if request.method == 'POST':
        siswa_data.nama = request.POST.get('nama')
        siswa_data.kelas = request.POST.get('kelas')
        siswa_data.nis = request.POST.get('nis')
        siswa_data.status = request.POST.get('status')
        
        # Simpan perubahan terupdate ke database SQLite
        siswa_data.save()
        
        # Lempar kembali secara otomatis ke halaman pertama (list_siswa)
        return redirect('list_siswa')
        
    # 3. Jika baru membuka halaman edit biasa, tampilkan form beserta data lamanya
    return render(request, 'app_perpus/edit_siswa.html', {'siswa': siswa_data})

# Halaman Hapus User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa # Pastikan nama model database kamu sesuai

from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa

def hapus_siswa(request, id):
    # 1. Ambil data objek siswa berdasarkan ID rute yang diklik
    siswa_data = get_object_or_404(Siswa, id=id)
    
    # 2. Jika tombol "Hapus" merah diklik (Mengirimkan request POST)
    if request.method == 'POST':
        siswa_data.delete() # Eksekusi perintah SQL hapus permanen dari SQLite
        return redirect('list_siswa') # Alihkan halaman kembali ke daftar utama user
        
    # 3. Tampilkan halaman konfirmasi jika baru diakses biasa (GET)
    return render(request, 'app_perpus/hapus_siswa.html', {'siswa': siswa_data})

from django.shortcuts import render, redirect
from django.db import connection

from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa # Pastikan nama model database kamu sesuai

def tambah_siswa(request):
    if request.method == 'POST':
        # Menangkap data dari form HTML kamu
        nama_form = request.POST.get('nama')
        kelas_form = request.POST.get('kelas')
        nis_form = request.POST.get('nis')
        status_form = request.POST.get('status')

        # Menyimpan data langsung ke Database/Model Siswa
        Siswa.objects.create(
            nama=nama_form,
            kelas=kelas_form,
            nis=nis_form,
            status=status_form
        )
        
        # Setelah sukses menyimpan, balikkan halaman ke daftar siswa
        return redirect('list_siswa') # Sesuaikan dengan name url daftarmu

    # Jika diakses biasa (GET), tampilkan form yang ada di folder app_perpus
    return render(request, 'app_perpus/tambah_siswa.html')
        
    # Jika methodnya GET (pertama kali buka halaman), tampilkan form tambah siswa
    return render(request, 'app_perpus/tambah_siswa.html')

# ==========================================
#              MODUL KELOLA BUKU
# ==========================================
 # 1. Menampilkan Daftar Buku
def list_buku(request):
    with connection.cursor() as cursor:
        # Mengambil semua baris data dari tabel buku
        cursor.execute("SELECT id, judul, pengarang, kategori, penerbit, tahun, rak, stok FROM buku;")
        columns = [col[0] for col in cursor.description]
        buku_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Mengirim data buku_list ke file template buku.html
    return render(request, 'app_perpus/buku.html', {'buku_list': buku_list})

# 2. Tambah Buku Baru
def add_buku(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun = request.POST.get('tahun')
        rak = request.POST.get('rak')
        stok = request.POST.get('stok')
        
        with connection.cursor() as cursor:
            # Eksekusi Query SQL INSERT menggunakan F-String super aman
            cursor.execute(f"""
                INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun, rak, stok)
                VALUES ('{judul}', '{pengarang}', '{kategori}', '{penerbit}', {int(tahun)}, '{rak}', {int(stok)});
            """)
            
        # Selesai menyimpan, langsung arahkan balik ke halaman utama daftar buku
        return redirect('list_buku')
        
    return render(request, 'app_perpus/tambah_buku.html')

# 3. Detail Buku
def detail_buku(request, id):
    with connection.cursor() as cursor:
        # Menggunakan sintaks format standar database python
        cursor.execute("SELECT id, judul, pengarang, kategori, penerbit, tahun, rak, stok FROM buku WHERE id = %s", [int(id)])
        row = cursor.fetchone()
        
        if row:
            columns = [col[0] for col in cursor.description]
            buku = dict(zip(columns, row))
            
            if "Laskar Pelangi" in buku['judul']:
                buku['isbn'] = "978-979-3062-79-2"
                buku['deskripsi'] = "Novel tentang perjuangan anak-anak Belitung mengejar pendidikan."
            elif "Bumi" in buku['judul']:
                buku['isbn'] = "978-602-0332-95-7"
                buku['deskripsi'] = "Kisah petualangan dunia paralel menegangkan bersama Raib, Seli, dan Ali."
            else:
                buku['isbn'] = "978-979-1227-43-8"
                buku['deskripsi'] = "Kisah inspiratif para santri Pondok Madani mengejar mimpi ke ujung dunia."
        else:
            buku = None

    return render(request, 'app_perpus/detail_buku.html', {'buku': buku})

 # 4. Edit Buku
def edit_buku(request, id):
    with connection.cursor() as cursor:
        # 1. KETIKA ADMIN KLIK TOMBOL "PERBARUI BUKU" (KIRIM DATA POST)
        if request.method == 'POST':
            judul = request.POST.get('judul')
            pengarang = request.POST.get('pengarang')
            kategori = request.POST.get('kategori')
            penerbit = request.POST.get('penerbit')
            tahun = request.POST.get('tahun')
            rak = request.POST.get('rak')
            stok = request.POST.get('stok')
            
            # Eksekusi Query UPDATE menggunakan F-String agar kebal dari eror formatting database
            cursor.execute(f"""
                UPDATE buku 
                SET judul = '{judul}', 
                    pengarang = '{pengarang}', 
                    kategori = '{kategori}', 
                    penerbit = '{penerbit}', 
                    tahun = {int(tahun)}, 
                    rak = '{rak}', 
                    stok = {int(stok)}
                WHERE id = {int(id)};
            """)
            
            # Selesai update, otomatis lempar kembali ke halaman tabel daftar buku
            return redirect('list_buku')
        
        # 2. KETIKA BARU MEMBUKA HALAMAN FORM EDIT (AMBIL DATA LAMA)
        else:
            # Gunakan F-String juga di sini untuk mengambil data lama berdasarkan ID
            cursor.execute(f"SELECT id, judul, pengarang, kategori, penerbit, tahun, rak, stok FROM buku WHERE id = {int(id)};")
            row = cursor.fetchone()
            
            if row:
                columns = [col[0] for col in cursor.description]
                buku = dict(zip(columns, row))
                
                # Logika penentu mockup deskripsi & isbn biar form terisi otomatis dengan cantik
                if "Laskar Pelangi" in buku['judul']:
                    buku['isbn'] = "978-979-3062-79-2"
                    buku['deskripsi'] = "Novel tentang perjuangan anak-anak Belitung mengejar pendidikan."
                elif "Bumi" in buku['judul']:
                    buku['isbn'] = "978-602-0332-95-7"
                    buku['deskripsi'] = "Kisah petualangan dunia paralel menegangkan bersama Raib, Seli, dan Ali."
                else:
                    buku['isbn'] = "978-979-1227-43-8"
                    buku['deskripsi'] = "Kisah inspiratif para santri Pondok Madani mengejar mimpi ke ujung dunia."
            else:
                return redirect('list_buku')

    return render(request, 'app_perpus/edit_buku.html', {'buku': buku})

# 5. Hapus Buku
def hapus_buku(request, id):
    with connection.cursor() as cursor:
        # 1. JIKA ADMIN MENEKAN TOMBOL MERAH "HAPUS" (KIRIM POST)
        if request.method == 'POST':
            # Jalankan query DELETE berdasarkan ID buku tersebut
            cursor.execute(f"DELETE FROM buku WHERE id = {int(id)};")
            # Kembali ke halaman daftar buku setelah terhapus
            return redirect('list_buku')
        
        # 2. JIKA BARU MEMBUKA HALAMAN UNTUK MELIHAT KONFIRMASI (GET)
        else:
            cursor.execute(f"SELECT id, judul FROM buku WHERE id = {int(id)};")
            row = cursor.fetchone()
            
            if row:
                columns = [col[0] for col in cursor.description]
                buku = dict(zip(columns, row))
            else:
                return redirect('list_buku')
                
    return render(request, 'app_perpus/hapus_buku.html', {'buku': buku})


# ==========================================
#              MODUL PEMINJAMAN
# ==========================================

# 1. Menampilkan Daftar Peminjaman
# 1. Menampilkan Semua Daftar Peminjaman
def list_peminjaman(request):
    with connection.cursor() as cursor:
        # Mengambil kolom nama_siswa dari database
        cursor.execute("SELECT id, nama_siswa, judul_buku, tanggal_pinjam, tanggal_kembali, keperluan, petugas, status FROM peminjaman;")
        rows = cursor.fetchall()
        
        peminjaman_list = []
        for row in rows:
            peminjaman_list.append({
                'id': row[0],
                'nama_siswa': row[1],
                'judul_buku': row[2],
                'tanggal_pinjam': row[3],
                'tanggal_kembali': row[4],
                'keperluan': row[5],
                'petugas': row[6],
                'status': row[7]
            })
            
    return render(request, 'app_perpus/list_peminjaman.html', {'peminjaman_list': peminjaman_list})

# 2. Mengubah Status Menjadi Dikembalikan (Tombol Centang)
def kembalikan_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE peminjaman SET status = 'Dikembalikan' WHERE id = {int(id)};")
    return redirect('list_peminjaman')


# 3. Menambahkan Data Peminjaman Baru
def tambah_peminjaman(request):
    if request.method == 'POST':
        nama_siswa = request.POST.get('nama_siswa')
        judul_buku = request.POST.get('judul_buku')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        tanggal_kembali = request.POST.get('tanggal_kembali')
        
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO peminjaman (nama_siswa, judul_buku, tanggal_pinjam, tanggal_kembali, status)
                VALUES ('{nama_siswa}', '{judul_buku}', '{tanggal_pinjam}', '{tanggal_kembali}', 'Dipinjam');
            """)
        return redirect('list_peminjaman')
        
    return render(request, 'app_perpus/tambah_peminjaman.html')

from django.shortcuts import render
from .models import Siswa

def user_list(request):
    # Mengambil seluruh data siswa dari database
    semua_siswa = Siswa.objects.all() 
    
    # Kirim data ke berkas template HTML dengan nama variabel 'daftar_user'
    return render(request, 'perpustakaan/user_list.html', {'daftar_user': semua_siswa})

# PASTIKAN FUNGSI INI ADA DI PALING BAWAH FILE VIEWS.PY KAMU:

from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa

# 1. VIEW UNTUK DETAIL USER
def detail_siswa(request, id):
    siswa_data = get_object_or_404(Siswa, id=id)
    # Merender template user_detail yang ada di dalam folder app_perpus

    return render(request, 'app_perpus/user_detail.html', {'siswa': siswa_data})