from tkinter import simpledialog

def authenticate(correct_password):
    password = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*')
    return password == correct_password
