import socket
import os
import threading # Wajib di-import untuk multithreading

# Pisahkan logika memproses klien ke dalam fungsi tersendiri
def tangani_klien(conn, addr):
    print(f"\n[+] Memulai thread baru untuk {addr}")
    try:
        # 1. Terima Header KTP (Format: TIPE|NAMA_FILE|UKURAN)
        header = conn.recv(1024).decode('utf-8')
        if not header:
            return
            
        tipe, nama_file, ukuran_str = header.split('|')
        ukuran = int(ukuran_str)
        
        # 2. Kirim sinyal "SIAP" ke klien
        conn.sendall(b"SIAP")
        
        # 3. Proses penerimaan berdasarkan TIPE
        bytes_diterima = 0
        
        if tipe == "TEXT":
            data_teks = b""
            while bytes_diterima < ukuran:
                chunk = conn.recv(4096)
                data_teks += chunk
                bytes_diterima += len(chunk)
            
            print(f"\n[+] PESAN TEKS DITERIMA DARI {addr}:")
            print(f"--- {nama_file} ---") 
            print(data_teks.decode('utf-8'))
            print("-" * 20)
            
        elif tipe == "FILE":
            # Tambahkan awalan alamat ip agar file dari klien berbeda tidak saling tindih
            ip_klien = addr[0].replace('.', '_')
            nama_simpan = f"terima_{ip_klien}_{nama_file}"
            print(f"\n[+] Menerima file dari {addr}: {nama_file} ({ukuran} bytes)")
            
            with open(nama_simpan, 'wb') as f:
                while bytes_diterima < ukuran:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_diterima += len(chunk)
                    
            print(f"[*] Selesai! File dari {addr} disimpan sebagai '{nama_simpan}'")

    except Exception as e:
        print(f"[!] Terjadi error pada koneksi {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Thread untuk {addr} telah selesai dan ditutup.")

def jalankan_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5000))
    # Boleh diisi 5 atau lebih. Ini adalah jumlah antrian jika semua "kasir/thread" sedang sibuk membuat koneksi.
    server.listen(5) 
    
    print("="*50)
    print("[*] SERVER UNICAST (MULTITHREAD) AKTIF")
    print("[*] Menunggu kiriman data dari banyak Client sekaligus...")
    print("="*50)

    while True:
        # Server hanya fokus menerima koneksi baru di loop utama ini
        conn, addr = server.accept()
        print(f"\n[+] Ada koneksi masuk dari {addr}")
        
        # Buat Thread (pekerja) baru khusus untuk menangani klien ini
        thread_klien = threading.Thread(target=tangani_klien, args=(conn, addr))
        # Jalankan thread-nya
        thread_klien.start()
        
        # Opsional: Melihat ada berapa thread yang sedang jalan (dikurangi 1 untuk main thread server)
        print(f"[*] Jumlah klien yang sedang ditangani bersamaan: {threading.active_count() - 1}")

if __name__ == "__main__":
    jalankan_server()