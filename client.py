#import library
import socket
import threading
import sqlite3
import hashlib
import customtkinter
from tkinter import *
from tkinter import messagebox

def mainlogin():
    def panel(username):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        root = customtkinter.CTk()
        root.geometry("500x350")
        root.title("tcp-chatroom")

        def connec():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('127.0.0.1', 6666))
                client.send(username.encode('utf-8'))
                for widget in root.winfo_children():
                    widget.destroy()

                def receive():
                    while True:
                        try:
                            mss = client.recv(1024).decode('utf-8')
                            list1.insert(END, mss + "\n")
                        except WindowsError as f:
                            print(f)
                            break

                def send():
                    mss = f'{username}: {entrysend.get()}'
                    client.send(mss.encode())

                def press(event):
                    send()

                list1 = customtkinter.CTkTextbox(master=root, width=400, height=315)
                list1.place(x=0, y=0)
                entrysend = customtkinter.CTkEntry(master=root, placeholder_text="Envoyer un message dans tcp-chatroom",
                                                   width=400)
                entrysend.place(x=0, y=320)
                buttonsend = customtkinter.CTkButton(master=root, text="Send", command=send)
                buttonsend.place(x=400, y=320)
                root.bind_all('<Return>', press)

                receive_thread = threading.Thread(target=receive)
                receive_thread.start()
            except Exception:
                messagebox.showinfo('serveur', 'serveur deconnecté')

        button14 = customtkinter.CTkButton(master=root, text="connect to chatroom", command=connec)
        button14.pack(expand=TRUE)

        root.mainloop()

    def login():
        password = hashlib.sha256(entry2.get().encode()).hexdigest()
        username = entry1.get()
        connn = sqlite3.connect("userdata.db")
        cur = connn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        if cur.fetchall():
            print("login successful!")
            root.destroy()
            panel(username)
            if username == 'admin': #donner les perms admin #password = 1234
                print('Permission administrateur')
                root.destroy()
                panel(username)
            else:
                root.destroy()
        else:
            print("login failed")

    def new_account():
        connec = sqlite3.connect("userdata.db")
        cur = connec.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
            id INTEGRER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
        username, password = entry1.get(), hashlib.sha256(entry2.get().encode()).hexdigest()
        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
        if username == '':
            entry1.delete(0, END)
            entry1.insert(0, "Failed")
        elif username == 'admin':
            entry1.delete(0, END)
            entry1.insert(0, "Failed")

        else:
            connec.commit()
            messagebox.showinfo('success!', 'compte crée avec succè')

    def press(event):
        login()

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("login-account")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill='both', expand=True)

    label1 = customtkinter.CTkLabel(master=frame, text='chatroom login', font=("Roboto", 24))
    label1.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    entry1.pack(pady=12, padx=10)
    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show='*')
    entry2.pack(pady=12, padx=10)

    button1 = customtkinter.CTkButton(master=frame, text="login", command=login)
    button1.pack(pady=12, padx=10)
    button2 = customtkinter.CTkButton(master=frame, text="create account", command=new_account)
    button2.pack(pady=12, padx=10)

    root.bind_all('<Return>',press)
    root.mainloop()
mainlogin()
