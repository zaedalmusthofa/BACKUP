'''*args'''

# memasukan data/arguments

def fungsi (nama,tinggi,berat):
    print(f"{nama} punya tinggi {tinggi} dan berat badan {berat}")

fungsi("walawe",170,65)

def fungsi(list_data):
    data = list_data.copy()
    nama = data[0]
    tinggi = data[1]
    berat = data[2]
    print(f"{nama} mempunyai tinggi {tinggi} dan berat badan {berat}")

fungsi(["adit",165,64])


# kenalan dengan *args

def fungsi(*args):
    nama = args[0]
    tinggi = args[1]
    berat = args[2]
    print(f"{nama} mempunyai tinggi {tinggi} dan berat badan {berat}")


fungsi("adit", 165, 64)

def tambah(*data):
    # data tipe datanya dalah tuple, dia bisa diiterasi
    output = 0
    for angka in data:
        output += angka

    return output

hasil = tambah(1,2,3,4,5,6,7,8,9)
print(f"Hasil = {hasil}")

hasil = tambah(10,5,15)
print(f"hasil = {hasil}")