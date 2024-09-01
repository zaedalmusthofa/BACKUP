'''Type Hints untuk fungsi'''

# bentuk dasr fungsi yang sudah dipelajari

'''
def fungsi(parameter):
    hasil = parameter**2
    print(hasil)

fungsi("walawe")
fungsi(1)
fungsi(True)
'''
# penggunaan type hints
import string
def sepuluh_pangkat(argument:int) -> int:
    output = 10**argument
    return output

hasil = sepuluh_pangkat(3)
print(hasil)

def display(argument:string):
    print(argument)

display("ucup")

import os

os.system("clear")
