# import

# fungsinya adalah untuk mengambil
# program dari file eksternal .py

# 1. untuk menyambung program dari eksternal
import program_print
import program_ucup

# 2. import dengan data
import variabel
import kucuy

# data ada di namespace variabel
print(variabel.data)
print(kucuy.data)

# 3. import dengan fungsi
import matematika
hasil = matematika.tambah(2,5)
print(hasil)