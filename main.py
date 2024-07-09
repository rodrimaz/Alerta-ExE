import tkinter as tk
from tkinter import simpledialog, messagebox
import schedule
import time
import threading
from alarms import AlarmManager
from auth import authenticate
import re
import os
import pystray
from PIL import Image, ImageDraw

class BetaAlertaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beta-Alerta")
        self.alarm_manager = AlarmManager()
        self.password = "4bio"  # Contraseña para configurar alarmas
        self.setup_ui()
        self.update_alarm_list()

        # Hacer la ventana invisible inicialmente
        self.root.withdraw()
        
        # Crear el icono en la bandeja del sistema
        self.create_tray_icon()

    def setup_ui(self):
        self.add_alarm_button = tk.Button(self.root, text="Agregar Alarma", command=self.add_alarm)
        self.add_alarm_button.pack(pady=20)

        self.alarm_list_frame = tk.Frame(self.root)
        self.alarm_list_frame.pack(pady=10)

    def update_alarm_list(self):
        for widget in self.alarm_list_frame.winfo_children():
            widget.destroy()

        for alarm in self.alarm_manager.alarms:
            frame = tk.Frame(self.alarm_list_frame)
            frame.pack(fill='x', pady=5)

            label = tk.Label(frame, text=f"{alarm['time']} - {alarm['url']}", anchor='w')
            label.pack(side='left', fill='x', expand=True)

            modify_button = tk.Button(frame, text="Modificar", command=lambda a=alarm: self.modify_alarm(a))
            modify_button.pack(side='right')

            delete_button = tk.Button(frame, text="Eliminar", command=lambda a=alarm: self.delete_alarm(a))
            delete_button.pack(side='right')

    def validate_time_format(self, time_str):
        pattern = re.compile(r"^\d{2}:\d{2}(:\d{2})?$")
        return pattern.match(time_str)

    def add_alarm(self):
        if authenticate(self.password):
            hour = simpledialog.askstring("Hora de la alarma", "Ingrese la hora (HH:MM):")
            if hour:
                if self.validate_time_format(hour):
                    url = simpledialog.askstring("URL de la alarma", "Ingrese el URL:")
                    if url:
                        self.alarm_manager.add_alarm(hour, url)
                        messagebox.showinfo("Alarma Agregada", f"Alarma configurada para las {hour} con URL: {url}")
                        self.update_alarm_list()
                    else:
                        messagebox.showerror("Error", "URL no proporcionado.")
                else:
                    messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM o HH:MM:SS.")
            else:
                messagebox.showerror("Error", "Hora no proporcionada.")
        else:
            messagebox.showerror("Error de autenticación", "Contraseña incorrecta")

    def delete_alarm(self, alarm):
        if authenticate(self.password):
            self.alarm_manager.remove_alarm(alarm['time'], alarm['url'])
            self.update_alarm_list()
            messagebox.showinfo("Alarma Eliminada", f"Alarma para las {alarm['time']} con URL: {alarm['url']} eliminada.")
        else:
            messagebox.showerror("Error de autenticación", "Contraseña incorrecta")

    def modify_alarm(self, alarm):
        if authenticate(self.password):
            new_hour = simpledialog.askstring("Modificar Hora de la alarma", "Ingrese la nueva hora (HH:MM):", initialvalue=alarm['time'])
            if new_hour:
                if self.validate_time_format(new_hour):
                    new_url = simpledialog.askstring("Modificar URL de la alarma", "Ingrese el nuevo URL:", initialvalue=alarm['url'])
                    if new_url:
                        self.alarm_manager.modify_alarm(alarm['time'], alarm['url'], new_hour, new_url)
                        messagebox.showinfo("Alarma Modificada", f"Alarma modificada a las {new_hour} con URL: {new_url}")
                        self.update_alarm_list()
                    else:
                        messagebox.showerror("Error", "URL no proporcionado.")
                else:
                    messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM o HH:MM:SS.")
            else:
                messagebox.showerror("Error", "Hora no proporcionada.")
        else:
            messagebox.showerror("Error de autenticación", "Contraseña incorrecta")

    def show_window(self, icon, item):
        icon.stop()
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon, item):
        icon.stop()
        self.root.quit()

    def create_image(self, width, height, color1, color2):
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        return image

    def create_tray_icon(self):
        image = self.create_image(64, 64, 'black', 'blue')
        menu = (pystray.MenuItem('Mostrar', self.show_window), pystray.MenuItem('Salir', self.quit_app))
        icon = pystray.Icon("BetaAlerta", image, "Beta-Alerta", menu)
        icon.run_detached()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Establecer el directorio de trabajo al inicio
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    app = BetaAlertaApp(root)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    root.mainloop()
