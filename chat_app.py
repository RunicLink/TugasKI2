# Nama file: chat_app.py

import socket
import sys
from des_logic import run_des  # Mengimpor fungsi DES dari file logic

# --- Konfigurasi ---
HOST = '127.0.0.1'  # Alamat localhost
PORT = 65432        # Port untuk koneksi
KEY = "mykey123"    # Kunci DES (HARUS 8 karakter dan SAMA di kedua device)
# --------------------

def start_server():
    """Berperan sebagai Device 1 (Server) - Menerima dulu, baru membalas."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"--- Device 1 (Server) ---")
        print(f"Kunci: {KEY}")
        print(f"Menunggu koneksi dari Device 2 di {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"Terhubung dengan Device 2 di {addr}")
            print("Ketik 'q' untuk keluar kapan saja.\n")

            while True:
                # 1. Menerima data terenkripsi dari Device 2
                data_hex = conn.recv(1024).decode('utf-8')
                if not data_hex:
                    print("Device 2 menutup koneksi.")
                    break
                
                # 2. Dekripsi data
                try:
                    decrypted_msg = run_des(data_hex, KEY, 'decrypt')
                    print(f"[Device 2]: {decrypted_msg}")
                    
                    if decrypted_msg.lower() == 'q':
                        print("Device 2 meminta keluar.")
                        break
                        
                except Exception as e:
                    print(f"Error dekripsi: {e}. Data diterima: {data_hex}")
                    continue # Lanjut ke loop berikutnya

                # 3. Mengirim balasan (Input, Enkripsi, Kirim)
                msg_to_send = input("[Device 1] Balas: ")
                encrypted_msg = run_des(msg_to_send, KEY, 'encrypt')
                conn.sendall(encrypted_msg.encode('utf-8'))
                
                if msg_to_send.lower() == 'q':
                    print("Menutup koneksi.")
                    break

def start_client():
    """Berperan sebagai Device 2 (Client) - Mengirim dulu, baru menerima balasan."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Gagal terhubung ke {HOST}:{PORT}. Pastikan Device 1 (Server) sudah berjalan.")
            return
            
        print(f"--- Device 2 (Client) ---")
        print(f"Kunci: {KEY}")
        print(f"Terhubung ke Device 1.")
        print("Ketik 'q' untuk keluar kapan saja.\n")

        while True:
            # 1. Mengirim pesan dulu (Input, Enkripsi, Kirim)
            msg_to_send = input("[Device 2] Kirim: ")
            encrypted_msg = run_des(msg_to_send, KEY, 'encrypt')
            s.sendall(encrypted_msg.encode('utf-8'))
            
            if msg_to_send.lower() == 'q':
                print("Menutup koneksi.")
                break

            # 2. Menerima balasan terenkripsi dari Device 1
            data_hex = s.recv(1024).decode('utf-8')
            if not data_hex:
                print("Device 1 menutup koneksi.")
                break

            # 3. Dekripsi balasan
            try:
                decrypted_msg = run_des(data_hex, KEY, 'decrypt')
                print(f"[Device 1]: {decrypted_msg}")
                
                if decrypted_msg.lower() == 'q':
                    print("Device 1 meminta keluar.")
                    break
                    
            except Exception as e:
                print(f"Error dekripsi: {e}. Data diterima: {data_hex}")
                continue # Lanjut ke loop berikutnya

if __name__ == "__main__":
    if len(KEY) != 8:
        print(f"Error: Kunci '{KEY}' harus tepat 8 karakter.")
        sys.exit(1)
        
    choice = input("Pilih peran Anda (1=Device 1/Server, 2=Device 2/Client): ").strip()
    
    if choice == '1':
        start_server()
    elif choice == '2':
        start_client()
    else:
        print("Pilihan tidak valid. Masukkan '1' atau '2'.")