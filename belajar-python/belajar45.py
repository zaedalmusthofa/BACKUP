'''Latihan Fungsi'''

import os

# program menghitung luas dan keliling persegi

# membuat header program
# os.system("clear") #ini untuk linux
# # os.system("cls") ini untuk windows
# print(f"{'PROGRAM MENGHITUNG LUAS':^40}")   # :^40 kode berfungsi agar kode berada di tengah dengan jarak 40
# print(f"{'DAN KELILING PERSEGI PANJANG':^40}")
# print(f"{'-'*40:^40}")
#
# # mengambil input user
# lebar = int(input("Lebar Persegi : "))
# panjang = int(input("Panjang persegi : "))
#
# keliling = 2*(lebar + panjang)
# luas = panjang*lebar
# print(f"keliling persegi = {keliling} dan luas persegi {luas}")

def header():
    '''fungsi Header'''
    os.system("clear") #ini untuk linux
    # os.system("cls") ini untuk windows
    print(f"{'PROGRAM MENGHITUNG LUAS':^40}")   # :^40 kode berfungsi agar kode berada di tengah dengan jarak 40
    print(f"{'DAN KELILING PERSEGI PANJANG':^40}")
    print(f"{'-'*40:^40}")

def input_user():
    # mengambil input user
    lebar = int(input("Lebar Persegi : "))
    panjang = int(input("Panjang persegi : "))

    return panjang,lebar

def hitung_luas(panjang,lebar):
    return panjang*lebar

def hitung_keliling(lebar,panjang):
    return 2*(lebar + panjang)

def display(massage,value):
    print(f"Hasil Perhitungan {massage} = {value}")

while True:
    header()

    PANJANG,LEBAR = input_user()
    LUAS = hitung_luas(LEBAR,PANJANG)
    KELILING = hitung_keliling(PANJANG,LEBAR)
    display("Luas",LUAS)
    display("Keliling",KELILING)
    iscontinue = input("apakah lanjut (y/n) ? ")
    if iscontinue == 'n':
        break

print("Program Selesai Terimakasih")
