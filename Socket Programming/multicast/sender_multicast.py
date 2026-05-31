import socket
import os
import time

# Konfigurasi IP Grup yang sama dengan receiver
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Buat socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Batasi jangkauan siaran (TTL = 1 berarti hanya di jaringan lokal ini saja)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

def kirim_teks(teks):
    # Format: TEXT|isinya
    payload = b"TEXT|" + teks.encode('utf-8')
    sock.sendto(payload, (MCAST_GRP, MCAST_PORT))
    print("[*] Pesan Multicast berhasil disiarkan!")

def kirim_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' tidak ditemukan.\n")
        return
        
    nama_file = os.path.basename(filepath)
    
    # 1. Beri aba-aba kalau file akan dikirim
    header_start = b"FILE_START|" + nama_file.encode('utf-8')
    sock.sendto(header_start, (MCAST_GRP, MCAST_PORT))
    
    print(f"[*] Mulai menyiarkan file {nama_file}...")
    time.sleep(0.5) # Beri waktu sejenak agar Receiver bersiap membuat file
    
    # 2. Kirim isi file sedikit demi sedikit
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4000) # Baca 4000 bytes saja agar aman
            if not chunk:
                break
            payload = b"CHUNK|" + chunk
            sock.sendto(payload, (MCAST_GRP, MCAST_PORT))
            
            # TRICK PENTING UDP: Beri jeda sangat kecil agar jaringan tidak tersedak (Packet Drop)
            time.sleep(0.002) 
            
    # 3. Beri aba-aba kalau file sudah selesai
    header_end = b"FILE_END|" + nama_file.encode('utf-8')
    sock.sendto(header_end, (MCAST_GRP, MCAST_PORT))
    print("[*] Siaran file Multicast selesai!\n")

if __name__ == "__main__":
    while True:
        print("="*40)
        print(" MENU PENGIRIMAN MULTICAST (A -> B,C) ")
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