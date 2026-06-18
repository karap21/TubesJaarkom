import socket
import struct

def jalankan_receiver():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    LOCAL_IP = '127.0.0.1' # Kunci di localhost

    # Inisialisasi socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind secara spesifik ke IP lokal dan Port
    sock.bind((LOCAL_IP, MCAST_PORT))

    # Mendaftar ke grup multicast khusus pada interface localhost
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(LOCAL_IP))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("="*50)
    print(f"[*] RECEIVER MULTICAST AKTIF")
    print(f"[*] Mendengarkan di jalur {LOCAL_IP}:{MCAST_PORT}")
    print("="*50)

    file_terbuka = None
    nama_simpan = ""

    while True:
        try:
            data, addr = sock.recvfrom(4100)

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