import socket
import os
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
LOCAL_IP = '127.0.0.1' # Kunci di localhost

# Inisialisasi socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Set TTL ke 1 (hanya untuk jaringan lokal)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

# PAKSA Loopback aktif (wajib agar bisa diterima di komputer sendiri)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# PAKSA agar data dikirim melalui jalur localhost, bukan adapter lain
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(LOCAL_IP))

def kirim_teks(teks):
    payload = b"TEXT|" + teks.encode('utf-8')
    sock.sendto(payload, (MCAST_GRP, MCAST_PORT))
    print("[*] Pesan Multicast berhasil disiarkan!\n")

def kirim_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] File '{filepath}' tidak ditemukan.\n")
        return
        
    nama_file = os.path.basename(filepath)
    
    header_start = b"FILE_START|" + nama_file.encode('utf-8')
    sock.sendto(header_start, (MCAST_GRP, MCAST_PORT))
    
    print(f"[*] Mulai menyiarkan file {nama_file}...")
    time.sleep(0.5) 
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4000) 
            if not chunk:
                break
            payload = b"CHUNK|" + chunk
            sock.sendto(payload, (MCAST_GRP, MCAST_PORT))
            time.sleep(0.002) 
            
    header_end = b"FILE_END|" + nama_file.encode('utf-8')
    sock.sendto(header_end, (MCAST_GRP, MCAST_PORT))
    print("[*] Siaran file Multicast selesai!\n")

if __name__ == "__main__":
    print(f"[*] SENDER MULTICAST AKTIF (Jalur: {LOCAL_IP})")
    while True:
        print("\n=== MENU MULTICAST ===")
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