## Global dan Local scope

nama_global = "otong" # <- ini variable global

# Akses Variable global dalam fungsi
def fungsi1():
    print(f"Funsi menampilkan {nama_global}")

fungsi1()

# Akses variabel global dalam loop
for i in range (0,5):
    print(f"Loop {i} - {nama_global}")

# Percabangan
if True:
    print(f"if menampilkan {nama_global}")

## Variabel Lokal Scope
def fungsi2():
    nama_local = "Ucup" # <- Variabel lokal scope

fungsi2()
# print(nama_local) # tidak bisa di gunakan

# Contoh 1: Penggunaan akses variabel

def say_otong():
    print(f"Hello {nama}")
nama = "Otong"
say_otong()

# Contoh 2: Merubah Variabel global
angka = 0
name = "Ucup"

def ubah(nila_baru, nama_baru):
    global angka# fungsi ini mendapat akses merubah angka
    global name
    angka = nila_baru
    name = nama_baru

print(f"Sebelum {angka,name}")
ubah(10,"Udin")
print(f"Sesudah = {angka, name}")

## Contoh 3:
angka = 0

for i in range(0,5):
    angka += i
    angka_dummy = 0

print(angka)
print(angka_dummy)

if True:
    angka = 10
    angka_dummy = 10

print(angka)
print(angka_dummy)