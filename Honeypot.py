import socket
import threading
import logging
from datetime import datetime
import openpyxl
from openpyxl import Workbook
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler("honeypot.log"), logging.StreamHandler()]
)

HOST = '0.0.0.0'
PORT = 2222

# Fake shell responses for some commands
FAKE_SHELL_RESPONSES = {
    "pwd": "/home/testuser",
    "ls": "Documents  Downloads  Music  Pictures  Videos",
    "whoami": "testuser",
    "id": "uid=1000(testuser) gid=1000(testuser) groups=1000(testuser)",
    "exit": "Bye!",
}

def save_session_to_excel(ip, username, password, commands):
    filename = "honeypot_log.xlsx"

    if os.path.exists(filename):
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["IP", "Username", "Password", "Commands"])

    commands_str = "\n".join(commands)
    ws.append([ip, username, password, commands_str])
    wb.save(filename)

def handle_client(conn, addr):
    ip, port = addr
    logging.info(f"[+] Connection from {ip}:{port} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    commands = []
    username = ''
    password = ''

    try:
        conn.sendall(b"login: ")
        username = conn.recv(1024).decode(errors='ignore').strip()

        conn.sendall(b"password: ")

        # Read password chars one by one, echo * to client, store real password
        password_bytes = b""
        while True:
            char = conn.recv(1)
            if not char or char in b"\r\n":
                break
            password_bytes += char
            conn.sendall(b'*')  # Echo * instead of real char

        password = password_bytes.decode(errors='ignore').strip()
        logging.info(f"[LOGIN] {ip}:{port} attempted login with Username: '{username}' | Password: '{password}'")

        conn.sendall(b"\nLogin successful.\n")
        conn.sendall(b"Welcome to Ubuntu 22.04.6 LTS (GNU/Linux 5.15.0 x86_64)\n")
        conn.sendall(b"$ ")

        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode(errors='ignore').strip()
            logging.info(f"[COMMAND] {ip}:{port} -> {command}")
            commands.append(command)

            if command.lower() == 'exit':
                conn.sendall(b'Bye!\n')
                break

            response = FAKE_SHELL_RESPONSES.get(command, f"bash: {command}: command not found")
            conn.sendall((response + '\n$ ').encode())

    except Exception as e:
        logging.error(f"[!] Error handling client {ip}:{port} - {e}")
    finally:
        conn.close()
        logging.info(f"[-] Connection closed from {ip}:{port}")

        # Save session to Excel
        save_session_to_excel(ip, username, password, commands)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        logging.info(f"Honeypot running on {HOST}:{PORT} - Ctrl+C to stop")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()

if __name__ == "__main__":
    start_server()
