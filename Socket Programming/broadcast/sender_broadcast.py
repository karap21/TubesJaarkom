import socket
import os
import time

BROADCAST_IP = '<broadcast>'
BROADCAST_PORT = 5008

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def kirim_teks(teks):
    payload = b"TEXT|" + teks.encode('utf-8')
    sock.sendto(payload, (BROADCAST_IP, BROADCAST_PORT))
    print("[*] Pesan Broadcast berhasil disebarkan ke semua!\n")

def kirim_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' tidak ditemukan.\n")
        return
        
    nama_file = os.path.basename(filepath)
    
    header_start = b"FILE_START|" + nama_file.encode('utf-8')
    sock.sendto(header_start, (BROADCAST_IP, BROADCAST_PORT))
    
    print(f"[*] Mulai mem-broadcast file {nama_file}...")
    time.sleep(0.5) 
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4000)
            if not chunk:
                break
            payload = b"CHUNK|" + chunk
            sock.sendto(payload, (BROADCAST_IP, BROADCAST_PORT))
            time.sleep(0.002) 
            
    header_end = b"FILE_END|" + nama_file.encode('utf-8')
    sock.sendto(header_end, (BROADCAST_IP, BROADCAST_PORT))
    print("[*] Broadcast file selesai!\n")

if __name__ == "__main__":
    while True:
        print("\n=== MENU BROADCAST ===")
        print("1. teks")
        print("2. file")
        print("0. keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            teks = input("Ketik pesan: ")
            kirim_teks(teks)
        elif pilihan == '2':
            nama_file = input("Nama file lengkap (contoh: tugas.pdf): ").strip('"').strip("'")
            kirim_file(nama_file)
        elif pilihan == '0':
            print("Keluar dari program.")
            break
        else:
            print("[!] Pilihan tidak valid.")