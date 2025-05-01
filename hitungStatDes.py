import numpy as np
import pandas as pd

# Function untuk input data
def inputData():
    data = [] 
    while True:
        try:
            nilai = float(input("Masukkan nilai data berupa angka: "))
            data.append(nilai)
        except ValueError:
            print("Input tidak valid. hanya angka yang diperbolehkan.")
            continue

        lanjut = input("Apakah ingin menambahkan data lagi? (y/n): ").lower()
        if lanjut != 'y':
            break
    return data 

