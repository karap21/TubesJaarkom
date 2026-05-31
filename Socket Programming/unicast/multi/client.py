import socket
import os

def kirim_data(tipe, label_atau_namafile, data_bytes):
    # Menyambungkan ke server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5000))
        
        # 1. Buat dan kirim Header (TIPE|NAMA_FILE/LABEL|UKURAN)
        ukuran = len(data_bytes)
        header = f"{tipe}|{label_atau_namafile}|{ukuran}"
        client.sendall(header.encode('utf-8'))
        
        # 2. Tunggu Server Siap
        balasan = client.recv(1024).decode('utf-8')
        if balasan == "SIAP":
            # 3. Kirim isi data
            client.sendall(data_bytes)
            print("[*] >> Pengiriman SUKSES! <<\n")
        else:
            print("[!] Server menolak pengiriman.\n")
            
    except ConnectionRefusedError:
        print("[!] Gagal terhubung. Pastikan server.py sudah jalan (running).\n")
    finally:
        client.close()

def kirim_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' tidak ditemukan di folder ini.\n")
        return
        
    nama_file = os.path.basename(filepath)
    print(f"[*] Sedang membaca dan mengirim file {nama_file}...")
    
    with open(filepath, 'rb') as f:
        data_bytes = f.read() # Membaca seluruh file menjadi bytes
        
    kirim_data("FILE", nama_file, data_bytes)

if __name__ == "__main__":
    while True:
        print("\n=== MENU ===")
        print("1. teks")
        print("2. file")
        print("0. keluar")
        
        # [PERBAIKAN 1]: Tambahkan input untuk memilih menu
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            teks = input("Ketik pesan: ")
            # [PERBAIKAN 2]: Tambahkan label "Pesan Teks" agar argumennya pas (3 parameter)
            kirim_data("TEXT", "Pesan Teks", teks.encode('utf-8'))
            
        elif pilihan == '2':
            nama_file = input("Nama file: ")
            kirim_file(nama_file)

        elif pilihan == '0':
            print("Keluar dari program.")
            break
            
        else:
            print("[!] Pilihan tidak valid.")