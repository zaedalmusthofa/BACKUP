"""**kwarg"""

def fungsi (nama,tinggi,berat):
    '''fungsi biasa'''
    print(f"{nama} pumya tinggi {tinggi} dan berat {berat}")

fungsi("denis",169,67)

def fungsi (**kwarg):
    '''fungsi biasa'''
    nama = kwarg["nama"]
    tinggi = kwarg["tinggi"]
    berat = kwarg["berat"]
    print(f"{nama} pumya timggi {tinggi} dan berat {berat}")

fungsi(nama="Denis",tinggi=178,berat=65)

def math(*args,**kwargs):
    output = 0
    if kwargs["option"] == "tambah":
        for angka in args:
            output +=angka
    elif kwargs["option"] == "perkalian":
        output = 1
        for angka in args:
            output *= angka

    else:
        print("tidak ada operasi")

    return output

hasil = math(1,2,3,4,5,6,option="tambah")
print(f"hasil jumlah {hasil}")
hasil = math(1,2,3,4,5,6,option="perkalian")
print(f"hasil kali {hasil}")