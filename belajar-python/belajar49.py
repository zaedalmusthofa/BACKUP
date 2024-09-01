def kuadrat(angka):
    return angka**2

print(f"Hasil Fungsi Kuadrat  = {kuadrat(5)}")
# Kita Coba dengan Lambda
# Output = lambda argument : expresion
kuadrat = lambda angka:angka**2
print(f"hasil lambda kuadrat = {kuadrat(4)}")

pangkat = lambda num,pow : num**pow
print(f"hasil lambda pangkat : {pangkat(4,2)}")

# Kegunaan Lambda Function

# Sorting untuk list Biasa
data_list = ["Otong","Ucup","Dudung"]
data_list.sort()
print(f"Sorted List = {data_list}")

# Sorting dia pakai panjang
def panjang_nama(nama):
    return len(nama)

data_list.sort(key=panjang_nama)
print(f"Sorted list by panjang = {data_list}")

# Sort Pakai lambda
data_list = ["Otong","Ucup","Dudung"]
data_list.sort(key=lambda nama: len(nama))
print(f"Sorted list by lambda = {data_list}")

# filter
data_angka = [1,2,3,4,5,6,7,8,9,10,11,12]

def kurang_dari_lima(angka):
    return angka < 5

data_angka_baru = list(filter(kurang_dari_lima,data_angka))
data_angka_baru = list(filter(lambda x:x<9,data_angka))
print(f"data angka baru = {data_angka_baru}")

# Kasus Genap
data_genap = list(filter(lambda x:x%2 == 0,data_angka))
print(data_genap)

# Kasus Ganjil
data_ganjil = list(filter(lambda x:x%2 == 1,data_angka))
print(data_ganjil)

# Kelipatan 3
data_3 = list(filter(lambda x:x%3 == 0,data_angka))
print(data_3)

# anonymos function
# curryin <- Huskell Curry

def pangkat(angka,n):
    hasil = angka**n
    return hasil

data_hasil = pangkat(3,3)
print(f"Fungsi Biasa = {data_hasil}")

# Dengan currying menjadi
def pangkat(n):
    return lambda angka:angka**n
pangkat_dua = pangkat(2)
print(f"pangkat 2 = {pangkat_dua(5)}")

pangkat_tiga = pangkat(3)
print(f"pangkat 3 = {pangkat_tiga(5)}")
print(f"pangkat bebas = {pangkat(3)(4)}")
