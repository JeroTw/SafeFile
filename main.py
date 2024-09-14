import os
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import customtkinter as ctk


def get_encryption_key(key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.BLAKE2b(digest_size=64),
        length=32,
        salt=b'github.com/JeroTw/SafeFile', 
        iterations=390000,
        backend=default_backend(),
    )
    lls = base64.urlsafe_b64encode(kdf.derive(str(key).encode()))
    return lls


def encrypt(message, key):
    encrypted = f.encrypt(message)
    return base64.urlsafe_b64encode(encrypted)


def decrypt(encrypted_message, key):
    try:
        decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_message))
        return decrypted
    except:
        pass


def iterate_files(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file == 'main.py' and root == path:
                continue
            yield os.path.join(root, file)


def process_files(mode, key):
    global f, log_text
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = Fernet(get_encryption_key(key))

    for file in iterate_files(current_dir):
        data = open(file, 'rb').read()
        if mode == 'e':
            if data.startswith(b'Z0FBQUF'):
                continue
            log_text.configure(text=f"Шифруем файл: {file}")
            data = encrypt(data, key)
            log_text.configure(text=f"Зашифрован файл: {file}")
        else:
            data = decrypt(data, key)
            log_text.configure(text=f"Дешифруем файл: {file}")
        if not data:
            log_text.configure(text=f"Неверный пароль: {file}")
            continue
        open(file, 'wb').write(data)
    log_text.configure(text=f"Обработка завершена!")


def on_click():
    mode = mode_var.get()
    key = key_entry.get()
    if mode == 'e':
        thread = threading.Thread(target=process_files, args=(mode, key))
        thread.start()
        label.configure(text="Шифрование начато...")
    elif mode == 'd':
        thread = threading.Thread(target=process_files, args=(mode, key))
        thread.start()
        label.configure(text="Дешифрование начато...")
    else:
        label.configure(text="Выберите режим!")





ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("SafeFile")

mode_frame = ctk.CTkFrame(app)
mode_frame.pack(pady=20)

mode_label = ctk.CTkLabel(mode_frame, text="Режим:")
mode_label.pack(side="left")

mode_var = ctk.StringVar(value='e')
mode_radio_e = ctk.CTkRadioButton(mode_frame, text="Шифрование", variable=mode_var, value='e')
mode_radio_e.pack(side="left")
mode_radio_d = ctk.CTkRadioButton(mode_frame, text="Дешифрование", variable=mode_var, value='d')
mode_radio_d.pack(side="left")

key_frame = ctk.CTkFrame(app)
key_frame.pack(pady=10)

key_label = ctk.CTkLabel(key_frame, text="Ключ:")
key_label.pack(side="left")

key_entry = ctk.CTkEntry(key_frame, width=200)
key_entry.pack(side="left")

button = ctk.CTkButton(app, text="Обработать", command=on_click)
button.pack(pady=10)


label = ctk.CTkLabel(app, text="")
label.pack()

log_text = ctk.CTkLabel(app, text="")
log_text.pack()




app.mainloop()
