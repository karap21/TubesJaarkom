import socket

def jalankan_receiver():
    BROADCAST_PORT = 5008

    # Membuat socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Mengizinkan penggunaan port yang sama di 1 laptop (untuk testing)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Mengizinkan socket ini menerima pesan broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Bind ke semua antarmuka ('0.0.0.0') di port 5008
    sock.bind(('0.0.0.0', BROADCAST_PORT))

    print("="*50)
    print(f"[*] RECEIVER BROADCAST AKTIF")
    print(f"[*] Menunggu siaran di port {BROADCAST_PORT}...")
    print("="*50)

    file_terbuka = None
    nama_simpan = ""

    while True:
        # Terima data (ukuran buffer 4100)
        data, addr = sock.recvfrom(4100)

        try:
            if data.startswith(b"TEXT|"):
                pesan = data[5:].decode('utf-8')
                print(f"\n[+] PENGUMUMAN BROADCAST DARI {addr}: \n{pesan}\n" + "-"*20)

            elif data.startswith(b"FILE_START|"):
                nama_file = data[11:].decode('utf-8')
                nama_simpan = f"bcast_terima_{nama_file}"
                file_terbuka = open(nama_simpan, 'wb')
                print(f"\n[*] Mulai menerima file broadcast: {nama_file}...")

            elif data.startswith(b"CHUNK|"):
                if file_terbuka is not None:
                    # Tulis isi file tanpa label 'CHUNK|'
                    file_terbuka.write(data[6:])

            elif data.startswith(b"FILE_END|"):
                if file_terbuka is not None:
                    file_terbuka.close()
                    file_terbuka = None
                    print(f"[+] Berhasil! File disimpan sebagai '{nama_simpan}'\n")
                    
        except Exception as e:
            print(f"[!] Error saat memproses data: {e}")

if __name__ == "__main__":
    jalankan_receiver()