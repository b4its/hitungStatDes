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

# Function untuk menghitung statistik berdasarkan distribusi frekuensi
def statistik_dari_distribusi(df):
    fi = df["Frekuensi"]
    xi = df["Titik Tengah"]
    
    N = fi.sum()
    mean = (fi * xi).sum() / N
    
    # Variansi dan Standar Deviasi
    var = ((fi * (xi - mean)**2).sum()) / (N - 1)
    std = np.sqrt(var)

    # Skewness
    skew_numerator = (fi * (xi - mean)**3).sum()
    skewness = skew_numerator / (N * (std**3))

    # Kurtosis (dengan excess kurtosis = kurtosis - 3)
    kurt_numerator = (fi * (xi - mean)**4).sum()
    kurtosis = (kurt_numerator / (N * (std**4))) - 3

    # Modus (menggunakan rumus interpolasi)
    modal_class_index = fi.idxmax()
    if modal_class_index > 0:
        L = float(df.loc[modal_class_index, "Interval"].split(" - ")[0])
        h = float(df.loc[modal_class_index, "Interval"].split(" - ")[1]) - L
        f1 = df.loc[modal_class_index, "Frekuensi"]
        f0 = df.loc[modal_class_index - 1, "Frekuensi"] if modal_class_index > 0 else 0
        f2 = df.loc[modal_class_index + 1, "Frekuensi"] if modal_class_index + 1 < len(df) else 0
        if (2*f1 - f0 - f2) != 0:
            modus = L + ((f1 - f0) / (2*f1 - f0 - f2)) * h
        else:
            modus = xi[modal_class_index]
    else:
        modus = xi[modal_class_index]

    # Median (interpolasi)
    cum_freq = fi.cumsum()
    median_class_index = cum_freq[cum_freq >= N/2].index[0]
    Lm = float(df.loc[median_class_index, "Interval"].split(" - ")[0])
    fm = df.loc[median_class_index, "Frekuensi"]
    F_before = cum_freq[median_class_index - 1] if median_class_index > 0 else 0
    h = float(df.loc[median_class_index, "Interval"].split(" - ")[1]) - Lm
    median = Lm + (((N/2 - F_before) / fm) * h)
    
    # Kuartil 1 (Q1)
    Q1_pos = N / 4
    q1_class_index = cum_freq[cum_freq >= Q1_pos].index[0]
    Lq1 = float(df.loc[q1_class_index, "Interval"].split(" - ")[0])
    fq1 = df.loc[q1_class_index, "Frekuensi"]
    Fq1 = cum_freq[q1_class_index - 1] if q1_class_index > 0 else 0
    hq1 = float(df.loc[q1_class_index, "Interval"].split(" - ")[1]) - Lq1
    Q1 = Lq1 + ((Q1_pos - Fq1) / fq1) * hq1

    # Kuartil 3 (Q3)
    Q3_pos = 3 * N / 4
    q3_class_index = cum_freq[cum_freq >= Q3_pos].index[0]
    Lq3 = float(df.loc[q3_class_index, "Interval"].split(" - ")[0])
    fq3 = df.loc[q3_class_index, "Frekuensi"]
    Fq3 = cum_freq[q3_class_index - 1] if q3_class_index > 0 else 0
    hq3 = float(df.loc[q3_class_index, "Interval"].split(" - ")[1]) - Lq3
    Q3 = Lq3 + ((Q3_pos - Fq3) / fq3) * hq3
    
    # menentukan jenis skewness
    jenisSkewness = "skewness belum ditentukan"
    if skewness > 0:
        jenisSkewness = "Positif Skewness"
    elif skewness == 0:
        jenisSkewness = "Normal Skewness"
    else:
        jenisSkewness = "Negatif Skewness"
    
    # menentukan jenis kurtosis
    jenisKurtosis = "kurtosis belum ditentukan"
    if skewness > 3:
        jenisKurtosis = "Leptokurtic"
    elif skewness == 0:
        jenisKurtosis = "Mesokurtic"
    else:
        jenisKurtosis = "Platykurtic"
        
    
    return {
        "Jumlah Data": N,
        "Mean": mean,
        "Modus": modus,
        "Median": median,
        "Variansi": var,
        "Kuartil 1": Q1,
        "Kuartil 3": Q3,
        "Standar Deviasi": std,
        "Skewness": skewness,
        "Jenis Skewness": jenisSkewness,
        "Kurtosis": kurtosis,
        "Jenis Kurtosis": jenisKurtosis
    }
