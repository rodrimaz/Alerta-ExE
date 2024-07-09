import schedule
import webbrowser
import tkinter as tk
import json
import os

class AlarmManager:
    def __init__(self):
        self.alarms = []
        self.alarm_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alarms.json')
        self.load_alarms()

    def add_alarm(self, time_str, url):
        schedule.every().day.at(time_str).do(self.trigger_alarm, url=url)
        self.alarms.append({"time": time_str, "url": url})
        self.save_alarms()

    def remove_alarm(self, time_str, url):
        self.alarms = [alarm for alarm in self.alarms if not (alarm["time"] == time_str and alarm["url"] == url)]
        schedule.clear(url)  # Clear the specific job
        self.save_alarms()

    def modify_alarm(self, old_time, old_url, new_time, new_url):
        self.remove_alarm(old_time, old_url)
        self.add_alarm(new_time, new_url)

    def trigger_alarm(self, url):
        # Abrir el URL en el navegador
        webbrowser.open(url)
        # Mostrar el mensaje con el enlace clickeable
        self.show_message(url)

    def show_message(self, url):
        root = tk.Tk()
        root.title("Alarma")
        
        # Establecer la ventana como topmost para asegurarse de que esté siempre al frente
        root.attributes('-topmost', True)
        
        def open_url(event):
            webbrowser.open(url)

        text = tk.Text(root, height=4, width=50)
        text.insert(tk.END, f"Haz clic aquí para abrir el enlace: {url}")
        text.tag_add("link", "1.28", "1.end")
        text.tag_config("link", foreground="blue", underline=1)
        text.tag_bind("link", "<Button-1>", open_url)
        text.pack(pady=20, padx=20)

        root.mainloop()

    def save_alarms(self):
        with open(self.alarm_file, 'w') as f:
            json.dump(self.alarms, f)

    def load_alarms(self):
        if os.path.exists(self.alarm_file):
            with open(self.alarm_file, 'r') as f:
                self.alarms = json.load(f)
                for alarm in self.alarms:
                    schedule.every().day.at(alarm["time"]).do(self.trigger_alarm, url=alarm["url"])
        else:
            self.alarms = []
            self.save_alarms()
