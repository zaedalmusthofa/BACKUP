'''Default argument'''

# def fungsi(argument)
# def fungsi( argument = nilai defaultnya)

def say_hello(nama = "ganteng"):
    '''fungsi dengan default argument'''
    print(f"Hello {nama}")
say_hello("ucup")
say_hello()

def sapa_dia(nama,pesan = "Apa kabar"):
    '''fungsi dengan satu input biasa,dan satu default argument'''
    print(f"Hai {nama} , {pesan}")
sapa_dia("Dudung","Hai ganteng")
sapa_dia("Ucup")

def hitung_pangkat(bilangan,pangkat):
    hasil = bilangan**pangkat
    print(f"pangkat dari {bilangan} dipangkatkan {pangkat} = {hasil}")
hitung_pangkat(5,3)

def pangkat(angka,pangkat=2):
    hasil = angka**pangkat
    return hasil
print(pangkat(4,3))

hasil = pangkat(5,3)
print(hasil)

def fungsi(input1=1,input2=2,input3=3,input4=4):
    hasil = input1+input2+input3+input4
    return hasil
print(fungsi())
print(fungsi(input1=4))