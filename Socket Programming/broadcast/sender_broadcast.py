import socket
import os
import time

BROADCAST_IP = '<broadcast>' # Otomatis menggunakan 255.255.255.255
BROADCAST_PORT = 5008

# Buat socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# WAJIB: Nyalakan izin broadcast pada socket pengirim
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def kirim_teks(teks):
    payload = b"TEXT|" + teks.encode('utf-8')
    sock.sendto(payload, (BROADCAST_IP, BROADCAST_PORT))
    print("[*] Pesan Broadcast berhasil disebarkan ke semua!")

def kirim_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' tidak ditemukan.\n")
        return
        
    nama_file = os.path.basename(filepath)
    
    # 1. Aba-aba mulai file
    header_start = b"FILE_START|" + nama_file.encode('utf-8')
    sock.sendto(header_start, (BROADCAST_IP, BROADCAST_PORT))
    
    print(f"[*] Mulai mem-broadcast file {nama_file} ke seluruh jaringan...")
    time.sleep(0.5) 
    
    # 2. Kirim chunk
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4000)
            if not chunk:
                break
            payload = b"CHUNK|" + chunk
            sock.sendto(payload, (BROADCAST_IP, BROADCAST_PORT))
            
            # Jeda agar router/jaringan tidak drop paket
            time.sleep(0.002) 
            
    # 3. Aba-aba selesai
    header_end = b"FILE_END|" + nama_file.encode('utf-8')
    sock.sendto(header_end, (BROADCAST_IP, BROADCAST_PORT))
    print("[*] Broadcast file selesai!\n")

if __name__ == "__main__":
    while True:
        print("="*40)
        print(" MENU PENGIRIMAN BROADCAST (A -> Semua) ")
        print("="*40)
        print("1. Kirim 1 - 5 kata")
        print("2. Kirim 1 kalimat panjang")
        print("3. Kirim 1 paragraf")
        print("4. Kirim file (txt, docx, pdf, jpg, mp3, mp4)")
        print("0. Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            teks = input("Ketik pesan 1-5 kata: ")
            kirim_teks(teks)
        elif pilihan == '2':
            teks = input("Ketik 1 kalimat panjang: ")
            kirim_teks(teks)
        elif pilihan == '3':
            teks = input("Ketik 1 paragraf: ")
            kirim_teks(teks)
        elif pilihan == '4':
            nama_file = input("Nama file / Absolute Path: ").strip('"').strip("'")
            kirim_file(nama_file)
        elif pilihan == '0':
            break
        else:
            print("[!] Pilihan tidak valid.")