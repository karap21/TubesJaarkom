import socket
import struct

def jalankan_receiver():
    # Konfigurasi IP Multicast (Harus di range 224.0.0.0 - 239.255.255.255)
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    # Membuat socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Izinkan beberapa program memakai port yang sama di 1 komputer (karena kita testing di 1 laptop)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind ke semua antarmuka jaringan pada port tersebut
    sock.bind(('0.0.0.0', MCAST_PORT))

    # Meminta sistem operasi untuk "Bergabung (Join)" ke grup Multicast
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("="*50)
    print(f"[*] RECEIVER MULTICAST AKTIF")
    print(f"[*] Bergabung di grup {MCAST_GRP}:{MCAST_PORT}")
    print("="*50)

    file_terbuka = None
    nama_simpan = ""

    while True:
        # Terima data (ukuran buffer 4100 bytes karena data kita potong per 4096)
        data, addr = sock.recvfrom(4100)

        try:
            if data.startswith(b"TEXT|"):
                pesan = data[5:].decode('utf-8')
                print(f"\n[+] PESAN DARI {addr}: \n{pesan}\n" + "-"*20)

            elif data.startswith(b"FILE_START|"):
                nama_file = data[11:].decode('utf-8')
                nama_simpan = f"mcast_terima_{nama_file}"
                file_terbuka = open(nama_simpan, 'wb')
                print(f"\n[*] Mulai mengunduh file multicast: {nama_file}...")

            elif data.startswith(b"CHUNK|"):
                if file_terbuka is not None:
                    # Tulis isi file tanpa label 'CHUNK|' (6 karakter pertama)
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