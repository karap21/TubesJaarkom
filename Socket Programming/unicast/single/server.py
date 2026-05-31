import socket
import os

def jalankan_server():
    # Membuat socket TCP IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5000))
    server.listen(1) # SINGLE THREAD: Hanya melayani 1 antrian pada satu waktu
    
    print("="*50)
    print("[*] SERVER UNICAST (SINGLE THREAD) AKTIF")
    print("[*] Menunggu kiriman data dari A...")
    print("="*50)

    while True:
        conn, addr = server.accept()
        
        try:
            # 1. Terima Header KTP (Format: TIPE|NAMA_FILE|UKURAN)
            header = conn.recv(1024).decode('utf-8')
            if not header:
                continue
                
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
                
                print(f"\n[+] PESAN TEKS DITERIMA:")
                print(f"--- {nama_file} ---") # nama_file di sini adalah label jenis pesan
                print(data_teks.decode('utf-8'))
                print("-" * 20)
                
            elif tipe == "FILE":
                # Tambahkan awalan 'terima_' agar file asli tidak tertimpa
                nama_simpan = f"terima_{nama_file}"
                print(f"\n[+] Menerima file: {nama_file} ({ukuran} bytes)")
                
                with open(nama_simpan, 'wb') as f:
                    while bytes_diterima < ukuran:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_diterima += len(chunk)
                        
                print(f"[*] Selesai! File berhasil disimpan sebagai '{nama_simpan}'")

        except Exception as e:
            print(f"[!] Terjadi error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    jalankan_server()