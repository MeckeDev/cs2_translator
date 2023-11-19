# You have to enable "-condebug" as a launch option and you may have to change the path to the CS2 directory

# if you want to contact me: https://linktr.ee/Mecke_Dev

import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from googletrans import Translator
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import os

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, translator, translated_file_path, output_text, language_var):
        super().__init__()
        self.translator = translator
        self.translated_file_path = translated_file_path
        self.translated_lines = set()
        self.output_text = output_text
        self.language_var = language_var

        # Load already translated lines from the file
        if os.path.exists(self.translated_file_path):
            with open(self.translated_file_path, "r", encoding="utf-8") as translated_file:
                self.translated_lines.update(translated_file.read().splitlines())

    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in reversed(lines):
            if ("[ALL] " in line or "[TEAM] " in line) and line not in self.translated_lines:
                username, message = line.split(": ", 1)
                dest_language = self.language_var.get()
                translated_message = self.translator.translate(message, dest=dest_language)
                translated_line = f'{username[15:]}: {translated_message.text} (from {languages[translated_message.src]})'

                # Update the GUI
                self.output_text.insert(tk.END, translated_line + '\n')
                self.output_text.see(tk.END)

                # Store the translated line in the set and the file
                self.translated_lines.add(line)
                with open(self.translated_file_path, "a", encoding="utf-8") as translated_file:
                    translated_file.write(line + '\n')
                break

def start_observer(console_log_path_var, output_text, language_var):
    path = console_log_path_var.get()
    translated_file_path = 'translated_lines.txt'

    translator = Translator()
    event_handler = LogFileHandler(translator, translated_file_path, output_text, language_var)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            root.update()  # Update the GUI
            time.sleep(1)  # Adjust the sleep interval as needed
            event_handler.process_file(os.path.join(path, 'console.log'))
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def clear_log(console_log_path_var):
    path = console_log_path_var.get()
    log_file_path = os.path.join(path, 'console.log')
    with open(log_file_path, 'w', encoding='utf-8'):
        pass

# Load languages from JSON
with open("languages.json", "r") as f:
    languages = json.load(f)

# Create GUI
root = tk.Tk()
root.title("Translation Log Viewer")

# Console log path input
console_log_path_var = tk.StringVar()
console_log_path_var.set(r'C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo')

path_label = tk.Label(root, text="Console Log Path:")
path_label.pack(pady=5)

path_entry = tk.Entry(root, textvariable=console_log_path_var, width=50)
path_entry.pack(pady=5)

# Language selection
language_var = tk.StringVar()
language_var.set("en")  # Set the default language to English

language_label = tk.Label(root, text="Select Language:")
language_label.pack(pady=5)

language_menu = ttk.Combobox(root, values=list(languages.values()), textvariable="English", state="readonly")
language_menu.pack(pady=5)

# Output text area
output_text = tk.Text(root, wrap="word", height=20, width=80)
output_text.pack(pady=10)

# Start observer button
start_button = tk.Button(root, text="Start Observer", command=lambda: start_observer(console_log_path_var, output_text, language_var))
start_button.pack(pady=10)

# Clear log button
clear_log_button = tk.Button(root, text="Clear Log", command=lambda: clear_log(console_log_path_var))
clear_log_button.pack(pady=10)

# Run the GUI
root.mainloop()
