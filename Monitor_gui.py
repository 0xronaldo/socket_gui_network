import socket
import tkinter as tk
from datetime import datetime

IP_MONITOR = "192.168.100.67"
PORT = 9300
LOG_FILE = "srv_log.txt"

def log_message(msg, msg_box):
    regmonitor = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{regmonitor} - {msg}\n"
    msg_box.insert(tk.END, line)
    msg_box.see(tk.END)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def check_notifications(s, msg_box, root):
    try:
        conn, addr = s.accept()
        msg = conn.recv(1024).decode()
        log_message(f"[MONITOR] Notificacion de {addr}: {msg}", msg_box)
        conn.close()
    except BlockingIOError:
        pass
    root.after(500, check_notifications, s, msg_box, root)

def start_monitor(msg_box, root):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(5)
    s.setblocking(False)
    log_message(f"[MONITOR] Escuchando en {IP_MONITOR}:{PORT}", msg_box)
    root.after(500, check_notifications, s, msg_box, root)

# Interfaz
root = tk.Tk()
root.title("Monitor")
msg_box = tk.Text(root, width=60, height=20)
msg_box.pack()

btn = tk.Button(root, text="Iniciar Monitor", command=lambda: start_monitor(msg_box, root))
btn.pack()

root.mainloop()
