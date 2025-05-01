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

# Function untuk membuat tabel distribusi frekuensi
def distribusiFrekuensi(data, bins='sturges'):
    if isinstance(bins, str):
        if bins == 'sturges':
            k = int(1 + 3.322 * np.log10(len(data)))
        else:
            raise ValueError("Hanya mendukung metode sturges.")
    else:
        k = bins

    frek, bin_edges = np.histogram(data, bins=k)
    intervals = [f"{round(bin_edges[i], 2)} - {round(bin_edges[i+1], 2)}" for i in range(len(bin_edges)-1)]
    kelas = [i+1 for i in range(len(intervals))]
    midpoints = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
    
    df = pd.DataFrame({
        "Kelas Ke": kelas,
        "Interval": intervals,
        "Titik Tengah": midpoints,
        "Frekuensi": frek
    })
    return df


