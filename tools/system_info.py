# tools/system_info.py
import platform
import psutil
import socket

def main():
    print(f"\nOS: {platform.system()} {platform.release()}")
    print(f"CPU: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"Disk: {round(psutil.disk_usage('/').total / (1024**3), 2)} GB total")